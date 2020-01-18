from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from oi_seattracker.models import Participant, Computer
import json

class Command(BaseCommand):
    help = 'Imports participants from a json file with array of [participant_id, full_name, computer_name] where computer_name can be null or just not be'

    def add_arguments(self, parser):
        parser.add_argument('--ignore-duplicates', action='store_true')
        parser.add_argument('source_file', type=open)

    def handle(self, *args, **options):
        data = json.load(options['source_file'])
        for line in data:
            uid = line[0]
            name = line[1]
            cid = line[2] if len(line) > 2 else None
            computer = None
            if cid is not None:
                computer = Computer.objects.get(nice_name=cid)
            Participant.objects.create(id=uid, full_name=name, computer=computer)
