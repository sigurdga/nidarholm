import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'nidarholm.settings'

path = '/srv/www/beta/nidarholm'
if path1 not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

