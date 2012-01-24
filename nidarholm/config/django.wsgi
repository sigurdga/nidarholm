import os
import sys
import site

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) #../..
site_packages = os.path.join(os.path.dirname(os.path.dirname(PROJECT_ROOT)), 'lib', 'python2.7', 'site-packages')

#site.addsitedir(site_packages)
sys.path.insert(0, site_packages)
sys.path.insert(0, PROJECT_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'nidarholm.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
