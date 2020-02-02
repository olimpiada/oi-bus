#!/usr/bin/env python3
import click
import os
from datetime import datetime

ANSIBLE_CONFIG='/etc/ansible/ansible-oi.cfg'
PLAYBOOKS='/usr/share/oi-bus/playbooks'

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
