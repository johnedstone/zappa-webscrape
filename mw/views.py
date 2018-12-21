from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render

from .harvest import indy_time
from .heavy_lifting import heavy_lifting


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

def baker_report():

    submit_id, results_timestamp = indy_time()

    heavy_lifting(
    submit_id=submit_id,
    mw_cron=True
    ) 

# vim: ai et ts=4 sw=4 sts=4 nu ru
