"""
WSGI config for wbg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys

import django.core.handlers.wsgi


sys.path.append('/var/wsgi')
sys.path.append('/var/wsgi/wbg')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbg.settings')

application = django.core.handlers.wsgi.WSGIHandler()
