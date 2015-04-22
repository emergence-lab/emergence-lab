from .base import *

# Debugging

DEBUG = False
TEMPLATE_DEBUG = False


# Authentication - Comment out for local LDAP no-TLS

# AUTH_LDAP_SERVER_URI = ''


# Misc Settings

ALLOWED_HOSTS += get_secret('ALLOWED_HOSTS')

# Media Files

MEDIA_URL = '/wsgi/media/'
MEDIA_ROOT = get_secret('MEDIA_ROOT')
SENDFILE_BACKEND = 'sendfile.backends.xsendfile'