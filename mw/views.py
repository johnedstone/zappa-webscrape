from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render


def simple(request):
    return HttpResponse("Hello {}".format(settings.USER[:2]))

def splash(request):

    context = {}

    return render(request, 'mw/splash.html', context)

def pan(request):

    results_path = 'https://{}/{}/{}.html'.format(
            settings.AWS_S3_CUSTOM_DOMAIN,
            settings.RESULTFILES_LOCATION,
            settings.RESULTFILE_NAME,
            )
    context = {'results_path': results_path}

    return render(request, 'mw/pan.html', context)
