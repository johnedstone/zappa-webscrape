#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import boto3
import base64


SECRET = os.getenv('SECRET')
DECRYPT = os.getenv('DECRYPT', 'off') == 'on'
KeyId = os.getenv('KeyId', 'alias/alias-name')
PROFILE_NAME = os.getenv('PROFILE_NAME', 'some aws credentials profile')

session = boto3.Session(profile_name=PROFILE_NAME)
dev_s3_client = session.client('kms', 'us-west-2')


if not DECRYPT:
    response = dev_s3_client.encrypt(KeyId=KeyId,Plaintext=SECRET.encode()) # us-west-2
    b = response['CiphertextBlob']
    print('{}'.format(base64.b64encode(b).decode('utf-8')))
else:
    print('{}'.format(dev_s3_client.decrypt(CiphertextBlob=base64.b64decode(SECRET))['Plaintext'].decode('utf8')))

# vim: ai et ts=4 sw=4 sts=4 ru nu
