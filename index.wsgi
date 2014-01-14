import os
import sys

sys.path.append( '/var/wsgi' )
sys.path.append( '/var/wsgi/wbg' )

os.environ['DJANGO_SETTINGS_MODULE'] = 'wbg.settings'

import django.core.handlers.wsgi
application = django.core.handlers.sgi.WSGIHandler( )

