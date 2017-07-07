from .base import *

# Debugging

DEBUG = get_secret('DEBUG', True)


# Misc Settings

ALLOWED_HOSTS += get_secret('ALLOWED_HOSTS', [])


# Authentication

AUTHENTICATION_BACKENDS = (
    get_secret(
        'AUTHENTICATION_BACKEND',
        'django.contrib.auth.backends.ModelBackend'
    ),
)


# Static Files

STATIC_ROOT = '/opt/django/static/'


# Media Files

MEDIA_URL = '{}/media/'.format(SUB_SITE)
MEDIA_ROOT = get_secret('MEDIA_ROOT', os.path.join(BASE_DIR, os.pardir, 'media'))
SENDFILE_BACKEND = 'sendfile.backends.nginx'
