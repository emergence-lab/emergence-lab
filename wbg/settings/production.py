from .base import *

# Debugging

DEBUG = False
TEMPLATE_DEBUG = False


# Authentication

AUTH_LDAP_SERVER_URI = ''


# Misc Settings

ALLOWED_HOSTS += get_secret('ALLOWED_HOSTS')
