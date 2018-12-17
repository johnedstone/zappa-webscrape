from django.urls import include, path, re_path
from django.http import HttpResponse

urlpatterns = [
    re_path('^$', lambda request:HttpResponse(
    '<div style="margin:2em;color:#005dab;'
    'font-style:italic;font-family:Tahoma,Verdana,sans-serif;">'
    'Hello World</div>'
    )),
    path('mw/', include('mw.urls')),
]

# vim: ai et ts=4 sw=4 sts=4 nu ru
