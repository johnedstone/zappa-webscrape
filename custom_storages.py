# custom_storages.py
# https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/ 
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

class ResultStorage(S3Boto3Storage):
    '''
    It would be nice to override this so, it doesn't take
    a full zappa role to write to S3, but very hard, and not
    recommended:
    https://github.com/Miserlou/Zappa/issues/984#issuecomment-313789220
    '''

    location = settings.RESULTFILES_LOCATION

# vim: ai et ts=4 sw=4 sts=4 nu ru
