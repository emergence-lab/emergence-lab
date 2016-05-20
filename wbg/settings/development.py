from .base import *


# Debugging

DEBUG = True


# Installed Apps

INSTALLED_APPS += (
    'debug_toolbar',
)


# Authentication

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


# Media Files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, 'media')
SENDFILE_BACKEND = 'sendfile.backends.development'
