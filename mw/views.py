from django.http import HttpResponse
from django.conf import settings


def simple(request):
    return HttpResponse("Hello {}".format(settings.USER[:2]))
