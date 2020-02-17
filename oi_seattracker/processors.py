import ipaddress
import json
import subprocess
import typing

from django.conf import settings
from django.http import HttpRequest

from .models import Computer


def get_mac_address(ip: str) -> typing.Optional[str]:
    try:
        ip = ipaddress.ip_address(ip)  # raises ValueError if invalid
        data = json.loads(
            subprocess.check_output(
                ["ip", "-j", "neigh", "show", str(ip)], universal_newlines=True
            )
        )
        assert len(data) == 1
        return data[0]["lladdr"]
    except (ValueError, KeyError, AssertionError) as _:
        return None


def computer_processor(request: HttpRequest) -> dict:
    return dict(computer=get_computer(request))


def some_settings_processor(request: HttpRequest) -> dict:
    return dict(EVERYONE_IS_ADMIN=settings.EVERYONE_IS_ADMIN, PRINTOUTS_ENABLED=settings.PRINTOUTS_ENABLED)


def get_computer(
        request: HttpRequest, create: bool = False
) -> typing.Optional[Computer]:
    ip_address = request.META["REMOTE_ADDR"]
    assert ip_address
    try:
        return Computer.objects.select_related('participant').get(ip_address=ip_address)
    except Computer.DoesNotExist:
        if create:
            return Computer.objects.select_related('participant').get_or_create(
                ip_address=ip_address,
                defaults=dict(mac_address=get_mac_address(ip_address)),
            )
        else:
            return None
