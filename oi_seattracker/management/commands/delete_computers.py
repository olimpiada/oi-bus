from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from oi_seattracker.models import Participant, Computer
import json

class Command(BaseCommand):
    help = 'Deletes all computers from database'

    def handle(self, *args, **options):
        Computer.objects.all().delete()
