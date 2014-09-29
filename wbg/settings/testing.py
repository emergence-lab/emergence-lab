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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


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