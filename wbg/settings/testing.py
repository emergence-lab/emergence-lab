import logging

from .base import *


# Debugging

DEBUG = False
TEMPLATE_DEBUG = False


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
PASSWORD_HASHER = ('django.contrib.auth.hashers.MD5PasswordHasher',)


# Model Mommy
MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.AutoSlugField': lambda: 'default-value',
}


# Media Files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, 'media')


# Test-only models
INSTALLED_APPS += (
    'core.tests',
)

REDIS_DB = 1

# Logging

logging.disable(logging.critical)

# File storages

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
