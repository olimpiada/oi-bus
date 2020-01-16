from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OiGhostwriterConfig(AppConfig):
    name = 'oi_ghostwriter'
    verbose_name = _('Printing and backups')
