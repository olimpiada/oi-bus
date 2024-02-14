from django.core.management.base import BaseCommand
from oi_seattracker.models import Participant

class Command(BaseCommand):
    help = 'Unassign the participant from the computer'
    
    def add_arguments(self, parser):
        parser.add_argument('participant_id', type=int)

    def handle(self, *args, **options):
        participant = Participant.objects.get(id=options['participant_id'])
        participant.computer = None
        participant.save()
