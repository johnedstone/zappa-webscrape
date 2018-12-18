# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import pytz

from django.conf import settings
from django.shortcuts import render

from .heavy_lifting import heavy_lifting

HUMAN_DATETIME  = "%A, %B %d, %Y at %H:%M:%S %z"

def indy_time():
    '''https://medium.com/@eleroy/10-things-you-need-to-know-about-date-and-time-in-python-with-datetime-pytz-dateutil-timedelta-309bfbafb3f7'''

    tz = pytz.timezone('America/New_York')
    return datetime.now(timezone.utc).astimezone(tz).strftime(HUMAN_DATETIME)


def harvest(request, fancy=True):

    submit_id = indy_time()
    context = {
        'submit_id': submit_id,
        'fancy': fancy,
        'results_path': 'https://{}/{}/{}'.format(
            settings.AWS_S3_CUSTOM_DOMAIN,
            settings.RESULTFILES_LOCATION,
            'results.html',
            ),
    }

    #heavy_lifting(submit_id=submit_id)

    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage
    fh = default_storage.open('results.html', 'w') # can not get this from settings for some reason
    fh.write(submit_id)
    fh.close()

    return render(request, 'mw/results.html', context)

# vim: ai et ts=4 sw=4 sts=4 nu ru
