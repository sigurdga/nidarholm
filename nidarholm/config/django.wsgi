import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'nidarholm.settings'

path1 = '/srv/www/beta/nidarholm'
path2 = '/srv/www/beta'
if path1 not in sys.path:
    sys.path.append(path1)
if path2 not in sys.path:
    sys.path.append(path2)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

