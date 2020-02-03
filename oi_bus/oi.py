#!/usr/bin/env python3
import click
import os
import json
from datetime import datetime
import functools

ANSIBLE_CONFIG='/etc/ansible/ansible-oi.cfg'
PLAYBOOKS='/usr/share/oi-bus/playbooks'
BACKUPDIR='/var/lib/oi-bus/golden'

opt_ask = None
opt_dry = False
default_ask = None

def should_ask(is_dangerous):
    def deco(f):
        def g(*args, **kwargs):
            global default_ask
            if default_ask is None:
                default_ask = is_dangerous
            f(*args, **kwargs)
        return functools.update_wrapper(g, f)
    return deco

@should_ask(True)
def ask_exec(cmd, env={}):
    env_diff = {}
    for k, v in env.items():
        if not k in os.environ:
            env_diff[k] = v
    os.environ.update(env_diff)

    with_env = ' '.join([f"{k}={v!r}" for k, v in env_diff.items()] + [repr(x) for x in cmd])

    ask = default_ask
    if opt_ask is not None:
        ask = opt_ask

    if opt_dry:
        print(with_env)
        return

    if not ask or click.confirm(f'Do you want to run {with_env} ?', default=True, err=True):
        os.execlp(cmd[0], *cmd)

@click.group()
@click.option('--ask/--no-ask', default=None, help="Enable / disable asking for confirmation")
@click.option('-n', '--dry-run', is_flag=True, help="Only print command that would be executed, but don't execute it")
def main(ask, dry_run : bool):
    global opt_ask, opt_dry
    opt_ask = ask
    opt_dry = dry_run

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('ansible_args', nargs=-1, type=click.UNPROCESSED)
def ansible(ansible_args):
    """Execute arbitrary Ansible ad hoc command in oi-bus configuration"""
    cmd = ['ansible'] + list(ansible_args)
    env = {'ANSIBLE_CONFIG': ANSIBLE_CONFIG}
    ask_exec(cmd, env)
main.add_command(ansible)

@click.command(name='ansible-playbook', context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('ansible_args', nargs=-1, type=click.UNPROCESSED)
def ansible_playbook(ansible_args):
    """Execute arbitrary Ansible playbook in oi-bus configuration"""
    cmd = ['ansible-playbook'] + list(ansible_args)
    env = {'ANSIBLE_CONFIG': ANSIBLE_CONFIG}
    ask_exec(cmd, env)
main.add_command(ansible_playbook)

@click.command()
@should_ask(False)
def check():
    """Test connection to all registered workstations"""
    ansible(['-m', 'ping', '--one-line', 'all'])
main.add_command(check)

@click.command()
@click.argument('cmd')
def execute(cmd: str):
    """Execute a shell command on all registered workstations"""
    ansible(['-m', 'shell', '-a', cmd, 'all'])
main.add_command(execute)

@click.command()
def reboot():
    """Reboot all registered workstations, blocking until they all come back
       If they don't within 10 minutes, raise an error.
    """
    ansible(['-m', 'reboot', 'all'])
main.add_command(reboot)

@click.command()
@click.argument('src')
@click.argument('dst', default=".")
@should_ask(False)
def upload(src, dst):
    """Upload local file SRC to all registered workstations as DST"""
    ansible(['-m', 'copy', '-a', f"src={src} dest={dst}", 'all'])
main.add_command(upload)

@click.command()
@click.argument('src')
@click.argument('dst', default=".")
@should_ask(False)
def download(src, dst):
    """Download file SRC from all registered workstations to a local directory DST"""
    ansible(['-m', 'fetch', '-a', f"src={src} dest={dst}", 'all'])
main.add_command(download)

@click.command()
@click.argument('dst', default="backupzaw")
@should_ask(False)
def backupzaw(dst):
    """Download source code files from zawodnik's home on all registered workstations to a local directory DST"""
    extensions = ['cpp', 'h', 'c', 'cc', 'pas', 'java', 'py']
    ext_cond = ' -o '.join(f"-name '*.{ext}'" for ext in extensions)
    date = datetime.now()
    tmpfile = f"/root/backupzaw-{date:%Y-%m-%d-%H-%M-%S}.tar.gz"
    dst = os.path.join(os.getcwd(), dst)
    ansible_playbook(['-e', f"filter={ext_cond!r} tmpfile='{tmpfile}' dstfile='{dst}'", os.path.join(PLAYBOOKS, 'backupzaw.yml')])
main.add_command(backupzaw)


@click.command()
@click.argument('hostname')
@click.argument('dst', default=None)
def backup(hostname, dst):
    """Bakcup whole filesystem of specified workstation """
    dst = os.path.join(dst or BACKUPDIR, hostname)
    try:
        os.mkdir(dst)
    except FileExistsError:
        pass
    rsync_opts = ['--numeric-ids', '-x', '--exclude', "'/tmp/*'", '--exclude', "'/tmp/.*'", '--exclude', "'/var/tmp/*'", '--exclude', "'/var/tmp/.*'"]
    if False:
        vars = {
            'ropts': rsync_opts,
        }
        ansible(['-m', 'synchronize', '-e', json.dumps(vars), '-a', f"archive=yes partial=yes delete=yes rsync_opts={{{{ropts}}}} mode=pull src=/ dest={dst!r}", hostname])
    else:
        ssh_opts="-t -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
        cmd = ['rsync', f"--rsh=/usr/bin/ssh {ssh_opts}", '-avP'] + rsync_opts + [f"root@{hostname}:/", dst]
        ask_exec(cmd)
main.add_command(backup)

@click.command()
@click.argument('updatedir')
@should_ask(False)
def update(updatedir):
    """[DEPRECATED] Upload update from directory UPDATEDIR to all workstations"""
    rsync_opts = ['-x', '--numeric-ids']
    try:
        os.chmod(os.path.join(updatedir, 'root'), 0o700)
    except FileNotFoundError:
        pass
    vars = {
        'ropts': rsync_opts,
    }
    ansible(['-m', 'synchronize', '-e', json.dumps(vars), '-a', f"archive=yes rsync_opts={{{{ropts}}}} checksum=yes src={updatedir!r} dest=/", 'all'])
main.add_command(update)

@click.command()
@click.argument('hostspec', default='all')
def shutdown(hostspec):
    """Shutdown specified (by default all registered) workstations with Wake On Lan"""
    ansible(['-a', 'poweroff', hostspec])
main.add_command(shutdown)


@click.command()
@click.argument('hostspec', default='all')
@should_ask(False)
def wake(hostspec):
    """Wake specified (by default all registered) workstations with Wake On Lan"""
    ansible_playbook(['-e', f"hostspec={hostspec!r}", os.path.join(PLAYBOOKS, 'wake.yml')])
main.add_command(wake)

if __name__ == '__main__':
    main()
