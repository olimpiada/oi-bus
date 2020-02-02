#!/usr/bin/env python3
import click
import os

ANSIBLE_CONFIG='/etc/ansible/ansible-oi.cfg'

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
