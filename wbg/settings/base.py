import json
import os

from django.core.exceptions import ImproperlyConfigured

import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType


# Filesystem Directories
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage' # For s3 store


# Secrets

with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())


def get_secret(setting, default=None, secrets_dict=secrets):
    """
    Get the secret variable or return exception.
    via Two Scoops of Django 1.6 pg 49
    """
    try:
        return secrets_dict[setting]
    except KeyError:
        if default is None:
            error_msg = 'Setting {0} is missing from the secrets file'.format(setting)
            raise ImproperlyConfigured(error_msg)
        else:
            return default


SECRET_KEY = get_secret('SECRET_KEY')


# Misc Settings

ALLOWED_HOSTS = []

ROOT_URLCONF = 'wbg.urls'

WSGI_APPLICATION = 'wbg.wsgi.application'

SUB_SITE = get_secret('SUB_SITE', '')


# User login

AUTH_USER_MODEL = 'core.User'
LOGIN_REDIRECT_URL = '{}/dashboard/'.format(SUB_SITE)
LOGIN_URL = "{}/accounts/login/".format(SUB_SITE)
LOGOUT_URL = "{}/accounts/logout/".format(SUB_SITE)


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, os.pardir, 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'core.context_processors.external_links',
                'core.context_processors.feedback',
                'messaging.context_processors.notifications',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]


# Installed Apps

INSTALLED_APPS = (
    # builtin apps
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # administration
    'grappelli',
    'django.contrib.admin',
    # # 3rd party apps
    'datetimewidget',
    'django_filters',
    'bootstrap3',
    'rest_framework',
    'rest_framework.authtoken',
    'ckeditor',
    'django_wysiwyg',
    'mptt',
    'storages',
    'django_ace',
    'django_rq',
    'crispy_forms',
    'simple_history',
    # local apps
    'core',
    'core.configuration',
    'dashboard',
    'journal',
    'd180',
    'afm',
    'hall',
    'project_management',
    'simulations',
    'schedule_queue',
    'sem',
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
    'simple_history.middleware.HistoryRequestMiddleware',
)


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DATABASE_NAME', 'db'),
        'USER': get_secret('DATABASE_USER', 'user'),
        'PASSWORD': get_secret('DATABASE_PASSWORD', ''),
        'HOST': get_secret('DATABASE_HOST', 'localhost'),
        'PORT': get_secret('DATABASE_PORT', 5432),
    }
}


# Authentication

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
}

AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''

AUTH_LDAP_USER_SEARCH = LDAPSearch(get_secret('AUTH_LDAP_USER_SEARCH', ''),
                                   ldap.SCOPE_SUBTREE, '(uid=%(user)s)')
AUTH_LDAP_USER_ATTR_MAP = {
    'email': 'mail',
    'full_name': 'sn',
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(get_secret('AUTH_LDAP_GROUP_SEARCH', ''),
                                    ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)')
AUTH_LDAP_GROUP_TYPE = PosixGroupType()

AUTH_LDAP_USER_FLAGS_BY_GROUP = get_secret('AUTH_LDAP_USER_FLAGS_BY_GROUP', {})

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Eastern'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, os.pardir, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, os.pardir, 'bower_components'),
)


# RESTful API

REST_FRAMEWORK = {
    # 'PAGINATE_BY': 25,
    'UPLOADED_FILES_USE_URL': False,
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

GITLAB_HOST = get_secret('GITLAB_HOST', 'localhost')
GITLAB_PRIVATE_TOKEN = get_secret('GITLAB_PRIVATE_TOKEN', '')


# Amazon Cloud

AWS_EC2_REGION = get_secret('AWS_EC2_REGION', '')
AWS_ACCESS_KEY_ID = get_secret('AWS_EC2_KEY', '')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_EC2_SECRET', '')
AWS_STORAGE_BUCKET_NAME = get_secret('AWS_S3_BUCKET', '')
S3_URL = 'https://{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)


# Redis

REDIS_HOST = get_secret('REDIS_HOST', 'localhost')
REDIS_PORT = get_secret('REDIS_PORT', 6379)
REDIS_DB = get_secret('REDIS_DB', 0)


# RQ

RQ_QUEUES = {
    'default': {
        'HOST': REDIS_HOST,
        'PORT': REDIS_PORT,
        'DB': REDIS_DB,
        'DEFAULT_TIMEOUT': 360,
    },
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H-%M-%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, os.pardir, 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propogate': True,
            'level': 'WARNING',
        },
        'rq.worker': {
            'handlers': ['file'],
            'propogate': True,
            'level': 'WARNING',
        },
        'emergence': {
            'handlers': ['file'],
            'propogate': True,
            'level': 'DEBUG',
        },
    },
}


# UploadFileHandlers

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'core.upload_handler.RQTemporaryFileUploadHandler',
)


# External Links

EXTERNAL_LINKS = get_secret('EXTERNAL_LINKS', [])


# Feedback

ENABLE_FEEDBACK = get_secret('ENABLE_FEEDBACK', False)


# Crispy Forms

CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Mendeley

ENABLE_MENDELEY = get_secret('ENABLE_MENDELEY', False)
MENDELEY_ID = get_secret('MENDELEY_ID', '')
MENDELEY_SECRET = get_secret('MENDELEY_SECRET', '')
MENDELEY_REDIRECT = get_secret('MENDELEY_REDIRECT', '')
MENDELEY_SSL_VERIFY = get_secret('MENDELEY_SSL_VERIFY', False)
