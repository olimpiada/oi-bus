"""oi_bus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from oi_seattracker import views as seattracker
from oi_ghostwriter import views as ghostwriter

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', seattracker.dashboard, name='dashboard'),
    url(r'^register$', seattracker.register, name='register'),
    url(r'^assign$', seattracker.assign, name='assign'),
    url(r'^healthcheck$', seattracker.healthcheck, name='healthcheck'),
    url(r'^ipauthsync/list$', seattracker.ipauthsync_list, name='ipauthsync_list'),

    url(r'^print$', ghostwriter.print, name='print'),
    url(r'^backups$', ghostwriter.backups, name='backups'),
    url(r'^backups/(?P<ident>\d+)$', ghostwriter.download_backup, name='download_backup'),
]

handler404 = 'oi_seattracker.views.teapot'
