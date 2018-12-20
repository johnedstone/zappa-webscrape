# -*- coding: utf-8 -*-
import io

from django.core.files.base import ContentFile
from custom_storages import FunWithStorage
from django.http import HttpResponse

def fun_with_storage(request):
    '''
    https://docs.djangoproject.com/en/2.1/howto/custom-file-storage/
    https://tartarus.org/james/diary/2013/07/18/fun-with-django-storage-backends

    Test:
    source venv/bin/activate
    source  local_vars_collectstatic.sh
    python manage.py shell

    from mw import fun_with_storage
    from django.test import RequestFactory

    request_factory = RequestFactory()
    request = request_factory.get('/path')
    fun_with_storage.fun_with_storage(request)
    '''

    fws = FunWithStorage()
    with io.StringIO() as fh:
        fh.write('Value: {}'.format('fun_with_storage'))
        path = fws.save('fun_with_storage.html', ContentFile(fh.getvalue().encode('utf-8')))

    return HttpResponse('Done writing out the file "fun_with_storage.html" in S3')

# vim: ai et ts=4 sw=4 sts=4 nu ru
