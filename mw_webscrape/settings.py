import os
import uuid

import base64
import boto3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RANDOM_NUMBER=str(uuid.uuid4()).lower().replace('-','')
SECRET_KEY = os.getenv('SECRET_KEY', RANDOM_NUMBER)

DEBUG = os.getenv('DEBUG', 'on') == 'on'
VARS_ENCRYPTED = os.getenv('VARS_ENCRYPTED', 'off') == 'on'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,*').split(',')

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'storages',
    'mw',
    ]
APPEND_SLASH = True

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mw_webscrape.urls'

WSGI_APPLICATION = 'mw_webscrape.wsgi.application'

DATABASES = {}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

CHROM_VERBOSITY = int(os.getenv('CHROM_VERBOSITY', '0'))  # 99 was the default
URL = os.getenv('URL')
USER = os.getenv('USER')
PW = os.getenv('PW')
DASHBOARD = os.getenv('DASHBOARD') # Can not navigate directly
ORDERS = os.getenv('ORDERS')

FRAMEWORK = os.getenv('FRAMEWORK', '')
if FRAMEWORK == 'Zappa' and VARS_ENCRYPTED:
    # settings for website to scrape
    USER = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(USER))['Plaintext'].decode('utf8')
    PW = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(PW))['Plaintext'].decode('utf8')

if not FRAMEWORK == 'Zappa' and not VARS_ENCRYPTED:
    # collectstatic, not zappa, but do, yes, interfere
    # so, only use when running collectstatic on the cli

    S3_USER_ACCESS_KEY_ID = os.getenv('S3_USER_ACCESS_KEY_ID')
    S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
    AWS_S3_REGION_NAME = os.getenv('REGION_NAME')
    AWS_ACCESS_KEY_ID = S3_USER_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = S3_SECRET_ACCESS_KEY

## collectstatic
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
# Tell django-storages the domain to use to refer to static files, for templates
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
# https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

RESULTFILES_LOCATION = 'results' # where it writes to in S3
DEFAULT_FILE_STORAGE = 'custom_storages.ResultStorage'

# Take Bucket ACLs
AWS_DEFAULT_ACL = None

# vim: ai et ts=4 sw=4 sts=4 nu ru
