import logging

from .base import *


# Debugging

DEBUG = True
TEMPLATE_DEBUG = True

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.FileHandler('debug.log'))
logger.setLevel(logging.DEBUG)
logger.propogate = True


# Authentication

AUTH_LDAP_SERVER_URI = 'ldap://localhost:9999'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}