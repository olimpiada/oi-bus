from django.contrib import admin

from .models import Backup, PrintRequest

@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ['owner', 'file', 'timestamp']

@admin.register(PrintRequest)
class PrintRequestAdmin(admin.ModelAdmin):
    pass
