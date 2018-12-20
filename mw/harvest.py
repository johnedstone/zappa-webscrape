# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import pytz

from django.conf import settings
from django.shortcuts import render

from .heavy_lifting import heavy_lifting, banner_page

HUMAN_DATETIME = "%a %b %-d %I:%M:%S %p %Y"
RESULTS_TIMESTAMP = "%Y%m%d-%H%M%S"

def indy_time():
    '''https://medium.com/@eleroy/10-things-you-need-to-know-about-date-and-time-in-python-with-datetime-pytz-dateutil-timedelta-309bfbafb3f7'''

    tz = pytz.timezone('America/New_York')
    submit_id = datetime.now(timezone.utc).astimezone(tz).strftime(HUMAN_DATETIME)
    results_timestamp = datetime.now(timezone.utc).astimezone(tz).strftime(RESULTS_TIMESTAMP) 


    return (submit_id, results_timestamp)


def harvest(request, fancy=True):

    submit_id, results_timestamp = indy_time()
    context = {
        'submit_id': submit_id,
        'fancy': fancy,
        'results_path': 'https://{}/{}/{}-{}.html'.format(
            settings.AWS_S3_CUSTOM_DOMAIN,
            settings.RESULTFILES_LOCATION,
            settings.RESULTFILE_NAME,
            results_timestamp,
            ),
    }

    banner_page(submit_id=submit_id, results_timestamp=results_timestamp)

    heavy_lifting(submit_id=submit_id, fancy=fancy,
        results_timestamp=results_timestamp)

    return render(request, 'mw/results.html', context)

# vim: ai et ts=4 sw=4 sts=4 nu ru
