from django.core.management.base import BaseCommand
from oi_seattracker.models import Participant
import json

class Command(BaseCommand):
    help = 'Remove assigned to participant computer'
    
    def add_arguments(self, parser):
        parser.add_argument('participant_id', type=int)

    def handle(self, *args, **options):
        try:
            participant = Participant.objects.get(id=options['participant_id'])
            participant.computer = None
            participant.save()
        except Participant.DoesNotExist:
            print(f'There is no participant with id {options["participant_id"]}.')
        except:
            print('Unexpected error happened.')
