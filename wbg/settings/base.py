import json
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TEMPLATE_CONTEXT_PROCESSORS
from django.core.exceptions import ImproperlyConfigured

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType


# Filesystem Directories
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Secrets

with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """
    Get the secret variable or return exception.
    via Two Scoops of Django 1.6 pg 49
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Setting {0} is missing from the secrets file'.format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret('SECRET_KEY')


# Misc Settings

ALLOWED_HOSTS = []

ROOT_URLCONF = 'wbg.urls'

WSGI_APPLICATION = 'wbg.wsgi.application'


# User login

AUTH_USER_MODEL = 'auth.User'
LOGIN_REDIRECT_URL = '/dashboard/'


# Templates

TEMPLATE_DIRS = (os.path.join(BASE_DIR, os.pardir, 'templates'), )
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)


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
    'core',
    'dashboard',
    'journal',
    'growths',
    'afm',
    'hall',
    'schedule_queue',
    # misc
    'actstream',
)


# Middleware

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Database

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': get_secret('DATABASE_NAME'),
        'USER': get_secret('DATABASE_USER'),
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
        'HOST': get_secret('DATABASE_HOST'),
        'PORT': get_secret('DATABASE_PORT'),
    }
}


# Authentication

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
}

AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''

AUTH_LDAP_USER_SEARCH = LDAPSearch(get_secret('AUTH_LDAP_USER_SEARCH'),
                                   ldap.SCOPE_SUBTREE, '(uid=%(user)s)')
AUTH_LDAP_USER_ATTR_MAP = {
    'email': 'mail',
    'first_name': 'sn',
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(get_secret('AUTH_LDAP_GROUP_SEARCH'),
                                    ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)')
AUTH_LDAP_GROUP_TYPE = PosixGroupType()

AUTH_LDAP_USER_FLAGS_BY_GROUP = get_secret('AUTH_LDAP_USER_FLAGS_BY_GROUP')

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True

AUTHENTICATION_BACKENDS = {
    'django_auth_ldap.backend.LDAPBackend',
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, os.pardir, 'static')
MEDIA_URL = '/wsgi/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, 'media')


# RESTful API

REST_FRAMEWORK = {
    'PAGINATE_BY': 25,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}


# Activity Stream

ACTSTREAM_SETTINGS = {
    'USE_JSONFIELD': True,
}


# Django WYSIWYG

DJANGO_WYSIWYG_FLAVOR = 'ckeditor'
CKEDITOR_UPLOAD_PATH = 'uploads/'


# Gitlab

GITLAB_HOST = get_secret('GITLAB_HOST')
GITLAB_PRIVATE_TOKEN = get_secret('GITLAB_PRIVATE_TOKEN')
