from django.urls import path, re_path
from django.http import HttpResponse

from . import views
from .harvest import harvest

urlpatterns = [
    # re_path('^$', lambda request:HttpResponse(
    # '<div style="margin:2em;color:#005dab;'
    # 'font-style:italic;font-family:Tahoma,Verdana,sans-serif;">'
    # 'Palindrome: Do Geese See God?</div>'
    # )),
    # path('', views.simple, name='simple'),
    path('', harvest, name='harvest'),
    path('plain/', harvest, {'fancy': False}, name='plain'),
    path('more/', views.simple, name='more'),
]

# vim: ai et ts=4 sw=4 sts=4 nu ru
