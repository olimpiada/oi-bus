import ipaddress
import json
import mimetypes
import os
import random
import subprocess
import typing
from pathlib import Path

from django.conf import settings
from django import forms
from django.db.models import Q, F
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_safe

from .models import Healthcheck, Participant, Computer, HEALTHCHECK_PARAMETERS
from .processors import get_computer, get_mac_address


@require_POST
@csrf_exempt
def healthcheck(request: HttpRequest) -> HttpResponse:
    computer = get_computer(request, create=True)
    print(request.POST)
    for param, _ in HEALTHCHECK_PARAMETERS:
        try:
            Healthcheck.objects.update_or_create(
                computer=computer,
                parameter=param,
                defaults=dict(timestamp=timezone.now(), value=float(request.POST[param])),
            )
        except (KeyError, ValueError) as e:
            pass
    return HttpResponse("")


def require_staff(f: typing.Callable[..., HttpResponse]) -> typing.Callable[..., HttpResponse]:
    def g(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not settings.EVERYONE_IS_ADMIN and not request.user.is_staff:
            return teapot(request)
        return f(request, *args, **kwargs)

    return g


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(model_to_dict(self.instance))
        if self.instance.ip_address:
            self.fields['ip_address'].disabled = True

    class Meta:
        model = Computer
        fields = ['ip_address', 'mac_address', 'nice_name', 'tags']


@require_staff
def register(request: HttpRequest) -> HttpResponse:
    initial = dict(ip_address=request.META['REMOTE_ADDR'],
                   mac_address=get_mac_address(request.META['REMOTE_ADDR']))
    if request.method == 'POST':
        form = RegisterForm(request.POST, initial=initial, instance=get_computer(request))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('assign'))
    else:
        form = RegisterForm(initial=initial, instance=get_computer(request))
    return render(request, "register.html", dict(form=form))


class AssignForm(forms.Form):
    computer = forms.ModelChoiceField(queryset=Computer.objects.all())
    participant = forms.ModelChoiceField(queryset=Participant.objects.all())

    def __init__(self, request: HttpRequest, computer: Computer):
        initial = dict(computer=computer)
        if hasattr(computer, 'participant'):
            initial['participant'] = computer.participant
        if request.method == 'POST':
            super().__init__(request.POST, initial=initial)
        else:
            super().__init__(initial=initial)
        self.fields['computer'].queryset = Computer.objects.filter(ip_address=computer.ip_address)
        # self.fields['computer'].disabled = True
        self.fields['participant'].queryset = Participant.objects.filter(
            Q(computer=computer) | Q(computer__isnull=True))


@require_staff
def assign(request: HttpRequest) -> HttpResponse:
    computer = get_computer(request)
    if not computer.ip_address:
        return render(request, "assign.html", dict(form=None))
    form = AssignForm(request, computer)
    if request.method == 'POST':
        if form.is_valid():
            participant = form.cleaned_data['participant']
            participant.computer = computer
            participant.save()
            return HttpResponseRedirect(reverse('dashboard'))
    return render(request, "assign.html", dict(form=form))


def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard.html")


def teapot(request: HttpRequest) -> HttpResponse:
    the_chosen_one = random.choice(os.listdir(settings.TEAPOT))
    with open(the_chosen_one, 'rb') as f:
        return HttpResponse(f, content_type=mimetypes.guess_type(the_chosen_one))


@require_safe
def ipauthsync_list(request: HttpRequest) -> HttpResponse:
    return JsonResponse(
        dict(
            mappings=list(Participant.objects.select_related("computer").annotate(
                user_id=F("id"), ip_address=F("computer__ip_address")
            ).filter(computer__isnull=False, ip_address__isnull=False).values('user_id', 'ip_address'))
        )
    )
