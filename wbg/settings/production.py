from .base import *

# Debugging

DEBUG = False
TEMPLATE_DEBUG = False


# Authentication

AUTH_LDAP_SERVER_URI = ''


# Misc Settings

ALLOWED_HOSTS += get_secret('ALLOWED_HOSTS')

# Media Files

MEDIA_URL = '/wsgi/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, 'media')
