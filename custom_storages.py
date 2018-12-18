# custom_storages.py
# https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/ 
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

class ResultStorage(S3Boto3Storage):
    location = settings.RESULTFILES_LOCATION

# vim: ai et ts=4 sw=4 sts=4 nu ru
