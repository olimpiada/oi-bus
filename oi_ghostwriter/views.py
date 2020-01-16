from django.http import HttpRequest, HttpResponseRedirect
from django.conf import settings
from django import forms
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_safe

from oi_seattracker.processors import get_computer
from oi_seattracker.models import Participant
from .models import Backup, PrintRequest

class UploadForm(forms.ModelForm):
    class Meta:
        model = Backup
        fields = ['owner', 'file']


def make_upload_form(request: HttpRequest, participant: Participant, print_ready: bool = False):
    form = None
    initial = dict(owner=participant)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, initial=initial)
    else:
        form = UploadForm(initial=initial)
    form.fields['owner'].queryset = Participant.objects.annotate(backup_count=Count('backups')).filter(pk=participant.pk, backup_count__lt=settings.MAX_PARTICIPANT_FILES)
    return form


def print(request: HttpRequest):
    computer = get_computer(request)
    user = computer.participant
    form = None
    files = PrintRequest.objects.filter(backup__owner=user)
    if files.count() < settings.MAX_PARTICIPANT_FILES:
        form = make_upload_form(request, user, True)
    if request.method == 'POST':
        if form.is_valid():
            backup = form.save()
            PrintRequest.objects.create(backup=backup).perform_printing_ritual()
            return HttpResponseRedirect(reverse('backups'))
    return render(request, 'print.html', dict(form=form))

def backups(request: HttpRequest):
    computer = get_computer(request)
    user = computer.participant
    form = None
    files = Backup.objects.filter(owner=user).order_by('-timestamp')
    if files.count() < settings.MAX_PARTICIPANT_FILES:
        form = make_upload_form(request, user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('backups'))
    return render(request, 'backup.html', dict(form=form, files=files))

@require_safe
def download_backup(request: HttpRequest, ident: str):
    computer = get_computer(request)
    ident: int = int(ident)
    backup = Backup.objects.get(owner=computer.participant, id=ident)
    backup.file.open()
    return HttpResponse(backup.file, content_type=mimetypes.guess_type(os.path.basename(backup.file.name))[0] or 'application/octet-stream')

