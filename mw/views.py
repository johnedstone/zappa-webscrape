from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render


def simple(request):
    return HttpResponse("Hello {}".format(settings.USER[:2]))

def splash(request):

    context = {}

    return render(request, 'mw/splash.html', context)
