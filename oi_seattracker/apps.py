from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OiSeattrackerConfig(AppConfig):
    name = 'oi_seattracker'
    verbose_name = _('Seat tracking')
