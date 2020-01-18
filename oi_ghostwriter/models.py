import os
import subprocess
import tempfile

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext as _imm

from oi_seattracker.models import Participant


class Backup(models.Model):
    owner = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="backups",
        verbose_name=_("Creator"),
    )
    file = models.FileField(verbose_name=_("File"))
    timestamp = models.DateTimeField(_("Upload time"), default=timezone.now)

    def __str__(self):
        return f"{self.file} (by {self.owner})"

    class Meta:
        verbose_name = _("participant uploaded file")
        verbose_name_plural = _("participant uploaded files")


class PrintRequest(models.Model):
    backup = models.OneToOneField(
        Backup,
        on_delete=models.CASCADE,
        related_name="print_request",
        verbose_name=_("Printed file"),
    )

    def perform_printing_ritual(self):
        backup = self.backup
        filename = os.path.basename(backup.file.name)
        self.backup.file.seek(0)
        file_contents = backup.file.read().decode('utf-8').encode('iso8859-2')
        tags = ', '.join(f'#{tag}' for tag in backup.owner.computer.tags.all())
        header = ' '.join([
            _imm('Participant:'),
            str(backup.owner),
            _imm('Computer:'),
            backup.owner.computer.nice_name,
            f'({tags})' if tags else '',
        ])
        a2ps = subprocess.run(['a2ps', f'--stdin={filename}', '-E', '-X', 'iso2', '-C', f'--pages=1-{settings.MAX_PRINT_PAGES}', f'--center-title={filename}', f'--header={header}'], input=file_contents, check=True)

    def __str__(self):
        return str(self.backup)

    class Meta:
        verbose_name = _("printed file")
        verbose_name_plural = _("printed files")

