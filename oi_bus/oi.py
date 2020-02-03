#!/usr/bin/env python3
import click
import os
import json
from datetime import datetime

ANSIBLE_CONFIG='/etc/ansible/ansible-oi.cfg'
PLAYBOOKS='/usr/share/oi-bus/playbooks'
BACKUPDIR='/var/lib/oi-bus/golden'

@click.group()
def main():
    pass

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('ansible_args', nargs=-1, type=click.UNPROCESSED)
def ansible(ansible_args):
    """Execute arbitrary Ansible ad hoc command in oi-bus configuration"""
    cmd = ['ansible'] + list(ansible_args)
    os.environ.setdefault('ANSIBLE_CONFIG', ANSIBLE_CONFIG)
    with_env = ' '.join(repr(x) for x in [f"ANSIBLE_CONFIG={ANSIBLE_CONFIG}"] + cmd)
    if click.confirm(f'Do you want to run {with_env}?', default=True, err=True):
        os.execlp('ansible', *cmd)
main.add_command(ansible)

@click.command(name='ansible-playbook', context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('ansible_args', nargs=-1, type=click.UNPROCESSED)
def ansible_playbook(ansible_args):
    """Execute arbitrary Ansible playbook in oi-bus configuration"""
    cmd = ['ansible-playbook'] + list(ansible_args)
    os.environ.setdefault('ANSIBLE_CONFIG', ANSIBLE_CONFIG)
    with_env = ' '.join(repr(x) for x in [f"ANSIBLE_CONFIG={ANSIBLE_CONFIG}"] + cmd)
    if click.confirm(f'Do you want to run {with_env}?', default=True, err=True):
        os.execlp('ansible-playbook', *cmd)
main.add_command(ansible_playbook)

@click.command()
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
def upload(src, dst):
    """Upload local file SRC to all registered workstations as DST"""
    ansible(['-m', 'copy', '-a', f"src={src} dest={dst}", 'all'])
main.add_command(upload)

@click.command()
@click.argument('src')
@click.argument('dst', default=".")
def download(src, dst):
    """Download file SRC from all registered workstations to a local directory DST"""
    ansible(['-m', 'fetch', '-a', f"src={src} dest={dst}", 'all'])
main.add_command(download)

@click.command()
@click.argument('dst', default="backupzaw")
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
        pretty_cmd = ' '.join(repr(x) for x in cmd)
        if click.confirm(f'Do you want to run {pretty_cmd}?', default=True, err=True):
            os.execlp('rsync', *cmd)
main.add_command(backup)

@click.command()
@click.argument('updatedir')
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
