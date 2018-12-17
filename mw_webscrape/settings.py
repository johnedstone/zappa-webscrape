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

CHROM_VERBOSITY = int(os.getenv('CHROM_VERBOSITY', '0'))  # 99 was the default
URL = os.getenv('URL')
USER = os.getenv('USER')
PW = os.getenv('PW')
DASHBOARD = os.getenv('DASHBOARD') # Can not navigate directly
ORDERS = os.getenv('ORDERS')
S3_USER_ACCESS_KEY_ID = os.getenv('S3_USER_ACCESS_KEY_ID')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')

FRAMEWORK = os.getenv('FRAMEWORK', '')
if FRAMEWORK == 'Zappa' and VARS_ENCRYPTED:
    # settings for website to scrape
    USER = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(USER))['Plaintext'].decode('utf8')
    PW = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(PW))['Plaintext'].decode('utf8')
    S3_USER_ACCESS_KEY_ID = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(S3_USER_ACCESS_KEY_ID))['Plaintext'].decode('utf8')
    S3_SECRET_ACCESS_KEY = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(S3_SECRET_ACCESS_KEY))['Plaintext'].decode('utf8')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_REGION_NAME = os.getenv('REGION_NAME')
AWS_ACCESS_KEY_ID = S3_USER_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = S3_SECRET_ACCESS_KEY

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Take Bucket ACLs
AWS_DEFAULT_ACL = None

# vim: ai et ts=4 sw=4 sts=4 nu ru
