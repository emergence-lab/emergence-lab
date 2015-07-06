import logging

from .base import *


# Debugging

DEBUG = True
TEMPLATE_DEBUG = True


# Installed Apps

INSTALLED_APPS += (
    'debug_toolbar',
    'nplusone.ext.django',
)


# Authentication

AUTH_LDAP_SERVER_URI = 'ldap://localhost:9999'


# Middleware

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'nplusone.ext.django.NPlusOneMiddleware',
)


# Logging

NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN


# Media Files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, 'media')
SENDFILE_BACKEND = 'sendfile.backends.development'
