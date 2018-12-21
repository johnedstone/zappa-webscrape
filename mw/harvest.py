# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import pytz

from django.conf import settings
from django.shortcuts import render

from .heavy_lifting import heavy_lifting, banner_page

HUMAN_DATETIME = "%a %b %-d %I:%M:%S %p %Y %Z"
RESULTS_TIMESTAMP = "%Y%m%d-%H%M%S"

def indy_time():
    '''https://medium.com/@eleroy/10-things-you-need-to-know-about-date-and-time-in-python-with-datetime-pytz-dateutil-timedelta-309bfbafb3f7'''

    tz = pytz.timezone('America/New_York')
    submit_id = datetime.now(timezone.utc).astimezone(tz).strftime(HUMAN_DATETIME)
    results_timestamp = datetime.now(timezone.utc).astimezone(tz).strftime(RESULTS_TIMESTAMP) 


    return (submit_id, results_timestamp)


def harvest(request, fancy=True, mw_cron=False):

    submit_id, results_timestamp = indy_time()

    if mw_cron:
        results_file_name = 'results.html'
    else:
        results_file_name = '{}-{}.html'.format(
            settings.RESULTFILE_NAME,
            results_timestamp,
            )


    results_path = 'https://{}/{}/{}'.format(
            settings.AWS_S3_CUSTOM_DOMAIN,
            settings.RESULTFILES_LOCATION,
            results_file_name,
            )

    context = {
        'submit_id': submit_id,
        'fancy': fancy,
        'results_path': results_path,
        'mw_cron': mw_cron,
    }

    if not mw_cron:
        banner_page(submit_id=submit_id, results_timestamp=results_timestamp)

    heavy_lifting(submit_id=submit_id, fancy=fancy,
        results_timestamp=results_timestamp,
        mw_cron=mw_cron,
        )

    return render(request, 'mw/results.html', context)

# vim: ai et ts=4 sw=4 sts=4 nu ru
