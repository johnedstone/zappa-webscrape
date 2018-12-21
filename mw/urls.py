from django.urls import path, re_path
from django.http import HttpResponse
from django.views.generic.base import RedirectView

from . import views
from .harvest import harvest
from .fun_with_storage import fun_with_storage

urlpatterns = [
    path('',  RedirectView.as_view(pattern_name='splash', permanent=False)),
    path('splash/', views.splash, name='splash'),
    path('harvest/', harvest, name='harvest'),
    path('plain/', harvest, {'fancy': False}, name='plain'),
    path('more/', views.simple, name='more'),
    path('fun-with-storage/', fun_with_storage, name='fun_with_storage'),
    path('mw-cron/', harvest, {'mw_cron': True}, name='mw_cron'),
    path('pan/', views.pan, name='pan'),
]

# vim: ai et ts=4 sw=4 sts=4 nu ru
