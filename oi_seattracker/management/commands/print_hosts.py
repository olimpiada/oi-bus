from django.core.management.base import BaseCommand, CommandError
from oi_seattracker.models import Computer
import json

class Command(BaseCommand):
    help = 'Prints hosts file format file'

    def handle(self, *args, **options):
        for host in Computer.objects.filter(nice_name__isnull=False, ip_address__isnull=False):
            print(f'{host.ip_address} {host.nice_name}')
