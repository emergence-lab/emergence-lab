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
    }
}


# Password hashing

PASSWORD_MANAGER = ('django.contrib.auth.hashers.MD5PasswordHasher',)


# Model Mommy
MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.AutoSlugField': lambda: 'default-value',
}

# Installed Apps

INSTALLED_APPS = (
    # builtin apps
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # administration
    'grappelli',
    'django.contrib.admin',
    # 3rd party apps
    'datetimewidget',
    'django_filters',
    'bootstrap3',
    'rest_framework',
    'rest_framework.authtoken',
    'ckeditor',
    'django_wysiwyg',
    'mptt',
    # local apps
    #'core',
    #'dashboard',
    #'journal',
    #'growths',
    #'afm',
    #'hall',
    'schedule_queue',
    # misc
    'actstream',
)