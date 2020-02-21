from django.core.management.base import BaseCommand, CommandError
from oi_seattracker.models import Computer, Tag, Participant
import json

class Command(BaseCommand):
    help = 'Prints ansible inventory'

    def add_arguments(self, parser):
        parser.add_argument('--list', action='store_true')

    def handle(self, *args, **options):
        obj = dict(_meta=dict(hostvars=dict()), all=dict(hosts=[]))
        for host in Computer.objects.all():
            obj['all']['hosts'].append(host.ansible_name)
            try:
                participant_id = host.participant.id
            except Participant.DoesNotExist:
                participant_id = None
            obj['_meta']['hostvars'][host.ansible_name] = dict(ansible_host=host.ip_address, mac_address=str(host.mac_address) if host.mac_address else None, participant_id=participant_id)
        for tag in Tag.objects.all():
            obj[tag.name] = dict(hosts=[host.ansible_name for host in tag.computer_set.all()])
        print(json.dumps(obj))
