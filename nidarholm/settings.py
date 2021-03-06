# encoding: utf-8

import os.path
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
#sys.path.append('/usr/lib/pymodules/python2.6') # hack to get pyexiv2 loaded on hylla server

# Django settings for nidarholm project.

DEVELOPMENT_MODE = False

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        ('Sigurd Gartmann', 'administrator@nidarholm.no'),
)

MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = True
DEFAULT_FROM_EMAIL = 'administrator@nidarholm.no'
SERVER_EMAIL = 'administrator@nidarholm.no'

MAIN_HOST = 'nidarholm.no' # used by mail server to pull updated email lists

DATABASES = {
    'default': {
        #'ENGINE':'sqlite3',
        #'NAME': '/srv/www/beta/nidarholm/database/development.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'nidarholm', # Or path to database file if using sqlite3.
        'USER': 'nidarholm', # Not used with sqlite3.
        'PASSWORD': 'niweb', # Not used with sqlite3.
        'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Default file size (in columns, where a column is 40px and margins are 20px
DEFAULT_IMAGE_SIZE = 4

# Serves local files, where permissions are checked

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/sigurdga/nidarholm/shared/media/'
FILE_SERVE_ROOT = MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.dirname(__file__)) + '/static-project/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$8k#7ze)v5wr5*e@ab7i+7*gu*va-!87y^ke!9uxx8j#_-z=f@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'request.middleware.RequestMiddleware',
    'permissions.middleware.http.Http403Middleware',
    'organization.middleware.OrganizationMiddleware',
    'pages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'nidarholm.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.dirname(__file__)) + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'south',
    'haystack',
    'request',
    'tagging',
    'tagging_autocomplete',
    'mptt',
    'profiles',
    'registration',
    'avatar',
    'markitup',
    'uni_form',
    'fileupload',
    'core',
    'search',
    'organization',
    'accounts',
    'events',
    'projects',
    #'forum',
    'news',
    'vault',
    'pages',
    'navigation',
    's7n.timeline',
    's7n.threaded_comments',
    's7n.forum',
    'samklang_utils',
    'floppyforms',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    )

AUTO_GENERATE_AVATAR_SIZES = (40,100,)
AVATAR_STORAGE_DIR = 'avatars/'
AVATAR_GRAVATAR_BACKUP = False
AVATAR_DEFAULT_URL = '/media/avatars/default.png'

#HAYSTACK_CONNECTIONS = {
    #'default': {
        #'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        #'PATH': '/home/sigurdga/nidarholm/shared/indexes/index.whoosh',
    #},
#}
HAYSTACK_SITECONF = 'search.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
#HAYSTACK_XAPIAN_PATH = '/home/sigurdga/nidarholm/shared/indexes/index.xapian'
HAYSTACK_WHOOSH_PATH = '/home/sigurdga/nidarholm/shared/indexes/index.whoosh'

MAX_TAG_LENGTH = 64 # reduce later
FORCE_LOWERCASE_TAGS = True # should replace with unidecoded space stripped versions

ACCOUNT_ACTIVATION_DAYS = 14
LOGIN_REDIRECT_URL = '/'

PAGINATION_DEFAULT_WINDOW = 8

COMMENTS_APP = "s7n.threaded_comments"
TIMELINE_APP = "s7n.timeline"

MARKITUP_FILTER = ('s7n.utils.markdown', {'safe_mode': True})
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_SKIN = 'markitup/skins/markitup'

try:
    from local_settings import *
except ImportError:
    pass
