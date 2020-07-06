# Django settings for gadai project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_ROOT = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db_gadai',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'indonesia',#'gsb3oktober',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

APPEND_SLASH=False

ALLOWED_HOSTS = ['']

TIME_ZONE = 'Asia/Jakarta'

LANGUAGE_CODE = 'id-ID'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

#USE_THOUSAND_SEPARATOR = True

NUMBER_GROUPING = 3

USE_TZ = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT,'static/')

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = os.path.join(PROJECT_ROOT,'/static/admin/')

ADMIN_MEDIA_PREFIX=  os.path.join(PROJECT_ROOT,'/static/admincss/')

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'u52vyz98o6y$6n+9+b7ldto3!+c1e90v37(!*b-)s8)6%cc@65'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    #'lockout.middleware.LockoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'gadai.middleware.login.RequireLoginMiddleware',
    'gadai.middleware.login.AutoLogout',
    'gadai.middleware.login.BlokingLogin',
)

ROOT_URLCONF = 'gadai.urls'

WSGI_APPLICATION = 'gadai.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT,'templates'),
    os.path.join(PROJECT_ROOT,'appkeuangan/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'gadai.appgadai','chosen',
    'gadai.xlsxwriter',
    'import_export',
    'gadai.django_pdf',
    'gadai.appkeuangan',
    #'django-lockout',
    #'twitter_bootstrap',
    #'bootstrap_toolkit',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTO_LOGOUT_DELAY = 30
#AUTO_LOGOUT_DELAY = 11130


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#SESSION_COOKIE_AGE = 4320000

AUTH_PROFILE_MODULE = 'appgadai.UserProfile'

try:
    from local_settings import*
except:
    pass

