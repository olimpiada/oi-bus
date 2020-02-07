from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from oi_ghostwriter.models import Backup
import json

class Command(BaseCommand):
    help = 'Deletes all computers from database'

    def handle(self, *args, **options):
        Backup.objects.all().delete()
