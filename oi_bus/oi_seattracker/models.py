from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from macaddress.fields import MACAddressField


class Tag(models.Model):
    name = models.SlugField()

    def __str__(self) -> str:
        return self.name


class Computer(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4', primary_key=True)
    mac_address = MACAddressField(null=True, blank=True)
    nice_name = models.SlugField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return '{name} ({ip_address})'.format(
            name=self.nice_name if self.nice_name else '<unknown>',
            ip_address=self.ip_address)


class Participant(models.Model):
    id = models.IntegerField(primary_key=True)
    full_name = models.TextField()
    computer = models.OneToOneField(Computer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.full_name} ({self.id})'


HEALTHCHECK_PARAMETERS = (
    ('loadavg', _('Load average')),
    ('numcpus', _('Processor count')),
    ('homefree', _('Home mountpoint free space')),
    ('ntfsfree', _('Host NTFS mountpoint free space')),
    ('ramfree', _('Free RAM memory')),
)


class Healthcheck(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    parameter = models.TextField(choices=HEALTHCHECK_PARAMETERS)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.BigIntegerField()

    class Meta:
        unique_together = (('computer', 'parameter'),)