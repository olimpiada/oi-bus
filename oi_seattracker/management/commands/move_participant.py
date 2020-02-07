from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from oi_seattracker.models import Participant, Computer
import json

class Command(BaseCommand):
    help = 'Move participant to a new computer'

    def add_arguments(self, parser):
        parser.add_argument('participant_id', type=int)
        parser.add_argument('new_computer', type=str)

    def handle(self, *args, **options):
        participant = Participant.objects.get(id=options['participant_id'])
        cid = options['new_computer']
        computer = Computer.objects.get(nice_name=cid)
        participant.computer = computer
        participant.save()
