from django.core.management.base import BaseCommand, CommandError
from oi_seattracker.models import Computer
import json

class Command(BaseCommand):
    help = 'Prints dhcp hostsfile for dnsmasq'

    def handle(self, *args, **options):
        for host in Computer.objects.filter(ip_address__isnull=False, mac_address__isnull=False):
            hostname = ""
            if host.hostname:
                hostname = f',{host.hostname}'
            print(f'{str(host.mac_address)},{str(host.ip_address)}{hostname}')
