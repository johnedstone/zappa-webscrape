# -*- coding: utf-8 -*-
import io

from zappa.async import task

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

@task
def heavy_lifting():

    with io.StringIO() as fh:
        fh.write('{}.\n'.format('woo hoo'))
        path = default_storage.save('results/query_results.html', ContentFile(fh.getvalue()))

    return

