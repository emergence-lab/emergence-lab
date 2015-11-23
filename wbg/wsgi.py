"""
WSGI config for wbg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import json
import os
import site
import sys

from django.core.exceptions import ImproperlyConfigured
from django.core.wsgi import get_wsgi_application

# Secrets

_BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(_BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())


def _get_secret(setting, secrets=secrets):
    """
    Get the secret variable or return exception.
    via Two Scoops of Django 1.6 pg 49
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = ('Setting {0} is missing from the '
                     'secrets file'.format(setting))
        raise ImproperlyConfigured(error_msg)

# End secrets

if _get_secret('PRODUCTION_MODE') == 'production':
    venv_path = _get_secret('VIRTUAL_ENV_PATH')
    sys_path = _get_secret('SYSTEM_PATH')

    site.addsitedir('{}/local/lib/python2.7/site-packages'.format(venv_path))

    sys.path.append(sys_path)
    sys.path.append(os.path.join(sys_path, _get_secret('SETTINGS_REL_ROOT')))

    activate_env = os.path.expanduser('{}/bin/activate_this.py'.format(venv_path))
    execfile(activate_env, dict(__file__=activate_env))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
        '{0}.settings.{1}'.format(_get_secret('SETTINGS_REL_ROOT'),
                                  _get_secret('PRODUCTION_MODE')))

    application = get_wsgi_application()
elif _get_secret('PRODUCTION_MODE') == 'docker':
    sys.path.append('/opt/django')
    sys.path.append('/opt/django/wbg')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbg.settings.base')

    import django.core.handlers.wsgi

    application = django.core.handlers.wsgi.WSGIHandler()
else:
    sys.path.append('/var/wsgi')
    sys.path.append('/var/wsgi/wbg')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbg.settings.base')

    import django.core.handlers.wsgi

    application = django.core.handlers.wsgi.WSGIHandler()
