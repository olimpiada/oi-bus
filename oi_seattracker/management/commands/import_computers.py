from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from oi_seattracker.models import Participant, Computer
import json

class Command(BaseCommand):
    help = 'Imports computers from a json file with array of [ip_address, nice_name, mac_address] where mac_address can be null or just not be'

    def add_arguments(self, parser):
        parser.add_argument('source_file', type=open)

    def handle(self, *args, **options):
        data = json.load(options['source_file'])
        for line in data:
            ip = line[0]
            name = line[1]
            mac = line[2] if len(line) > 2 else None
            Computer.objects.create(ip_address=ip, nice_name=name, mac_address=mac)
