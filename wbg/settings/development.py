import logging

from .base import *


# Debugging

DEBUG = True
TEMPLATE_DEBUG = True

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.FileHandler('debug.log'))
logger.setLevel(logging.DEBUG)
logger.propogate = True


# Installed Apps

# INSTALLED_APPS += ('debug_toolbar', )


# Authentication

AUTH_LDAP_SERVER_URI = 'ldap://localhost:9999'


# Middleware

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
