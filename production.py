import os.path

# Django settings for nidarholm project.

DEVELOPMENT_MODE = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        ('Sigurd Gartmann', 'sigurdga-django@sigurdga.no'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/srv/www/beta/nidarholm/database/development.sqlite3', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
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
FILE_SERVE_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/uploads/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/srv/www/beta/nidarholm/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/m/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'sqlmiddleware.SQLLogToConsoleMiddleware',
    'request.middleware.RequestMiddleware',
    'permissions.middleware.http.Http403Middleware',
    'pages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'nidarholm.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.dirname(__file__)) + '/templates',
    #os.path.abspath(os.path.dirname(__file__)) + '/../django-debug-toolbar/debug_toolbar/templates',
)

INSTALLED_APPS = (
    'accounts',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'south',
    'request',
    'tagging',
    'profiles',
    'avatar',
    #'debug_toolbar',
    'relations',
    'events',
    'forum',
    'news',
    'vault',
    'pages',
    'navigation',
    #'instruments',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    )

AUTO_GENERATE_AVATAR_SIZES = (100,)
AVATAR_STORAGE_DIR = 'avatars/'
AVATAR_GRAVATAR_BACKUP = False
AVATAR_DEFAULT_URL = 'avatars/dragen.jpg'