from django.contrib import admin
from .models import Computer, Participant, Healthcheck, Tag


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('nice_name', 'ip_address', 'mac_address')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'computer')


@admin.register(Healthcheck)
class HealthcheckAdmin(admin.ModelAdmin):
    list_display = ('computer', 'parameter', 'timestamp', 'value')
    list_display_links = ('computer', 'parameter')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
