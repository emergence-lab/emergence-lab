from .base import *

# Debugging

DEBUG = False
TEMPLATE_DEBUG = False


# Misc Settings

ALLOWED_HOSTS += get_secret('ALLOWED_HOSTS')


# Media Files

MEDIA_URL = '/wsgi/media/'
MEDIA_ROOT = get_secret('MEDIA_ROOT')
SENDFILE_BACKEND = 'sendfile.backends.xsendfile'


# Templates

TEMPLATE_LOADERS = ('django.template.loaders.cached.Loader',) + TEMPLATE_LOADERS


# Sessions

SESSION_ENGINE 'django.contrib.sesstions.backend.cache'
