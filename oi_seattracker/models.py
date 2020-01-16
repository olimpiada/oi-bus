from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from macaddress.fields import MACAddressField


class Tag(models.Model):
    name = models.SlugField(_('Name'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('computer group')
        verbose_name_plural = _('computer groups')


class Computer(models.Model):
    ip_address = models.GenericIPAddressField(_('IP address'), protocol='IPv4', primary_key=True)
    mac_address = MACAddressField(_('MAC address'), null=True, blank=True)
    nice_name = models.SlugField(_('Internal hostname'), null=True, blank=True, help_text=_('This will be used to generate SSH client configuration to make it easier to connect for troubleshooting.'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('Groups'), help_text=_('This will be used to generate Ansible host groups for easier managing. Groups are also printed on participant printouts. For locations with multiple participant rooms it is recommended to at least create a group for every room and assign it to the computers in that room to make printout delivery easier.'))

    def __str__(self) -> str:
        return '{name} ({ip_address})'.format(
            name=self.nice_name if self.nice_name else '<unknown>',
            ip_address=self.ip_address)

    class Meta:
        verbose_name = _('computer')
        verbose_name_plural = _('computers')


class Participant(models.Model):
    id = models.IntegerField(_('Participant ID'), primary_key=True, help_text=_('This is an numeric ID assigned to the participant by the central administration of the competition. It is used to associate participant\'s onsite workstation with their SIO2 account.'))
    full_name = models.TextField(_('Full name'))
    computer = models.OneToOneField(Computer, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Assigned computer'))

    def __str__(self) -> str:
        return f'{self.full_name} ({self.id})'

    class Meta:
        verbose_name = _('participant')
        verbose_name_plural = _('participants')


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
    value = models.FloatField()

    class Meta:
        unique_together = (('computer', 'parameter'),)
        verbose_name = _('healthcheck')
        verbose_name_plural = _('healthchecks')
