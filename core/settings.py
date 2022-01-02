"""
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os, re
import logging.config
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', default=True, cast=bool)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

ADMIN_URL = 'admin/'
APPEND_SLASH = True
THOUSAND_SEPARATOR = ' '
SITE_NAME = 'Valère Obei'
USE_THOUSAND_SEPARATOR = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PACKAGE_APPS = [
    'jet.dashboard',
    'jet',
    'django_summernote',
    'django.contrib.admin',

    'import_export',
    'widget_tweaks',
    'django_filters',
    'phonenumber_field',
    'compressor',
]

CUSTOM_APPS = [
]

INSTALLED_APPS += PACKAGE_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATE_DIR = str(BASE_DIR / 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "SAMEORIGIN"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': 5432,
            'ATOMIC_REQUESTS': True
        }
    }

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.mysql",
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
            'ATOMIC_REQUESTS': True
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'max_similarity': 0.9}},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 9}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Hashage des donnees
# https://docs.djangoproject.com/fr/3.1/ref/settings/

DEFAULT_HASHING_ALGORITHM = 'sha1'

# password hashers
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
# https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

USE_TZ = False
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'fr'
USE_I18N = USE_L10N = True
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%d-%m-%Y')

# staticfiles finders
# See: https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#staticfiles-finders

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # django compressor staticfiles
    'compressor.finders.CompressorFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# https://docs.djangoproject.com/fr/4.0/ref/settings/#message-tags
# Messages built-in framework

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Phone Number Config
# https://pypi.org/project/django-phonenumber-field/

PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

# Django-compressor config
# https://django-compressor.readthedocs.io/en/stable/settings/#settings

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_OUTPUT_DIR = "cache"
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_REBUILD_TIMEOUT = 5400
COMPRESS_PRECOMPILERS = (
    ("text/less", "/usr/local/bin/lessc {infile} {outfile}"),
    ("text/x-sass", "/usr/local/bin/sass {infile} {outfile}"),
    ("text/x-scss", "/usr/local/bin/sass {infile} {outfile}"),
)
COMPRESS_OFFLINE_CONTEXT = {
    "STATIC_URL": "STATIC_URL",
}

# https://docs.djangoproject.com/fr/3.2/ref/settings/#ignorable-404-urls

IGNORABLE_404_URLS = [
    re.compile(r'^/cpc/'),
    re.compile(r'^/cpanel/'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
    re.compile(r'\.(cgi|php|pl)$'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
]

DISALLOWED_USER_AGENTS = [
    re.compile(r'^NaverBot.*'),
    re.compile(r'^EmailSiphon.*'),
    re.compile(r'^SiteSucker.*'),
    re.compile(r'^sohu-search'),
]

# Configuration django-jet
# https://jet.readthedocs.io/en/latest/config_file.html

JET_THEMES = [
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

# Show summernote with Bootstrap4

SUMMERNOTE_THEME = 'bs4'

SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'airMode': True,
        'width': '75%',
        'height': '300',
        'toolbar': [
            [
                'font', [
                    'bold', 'italic', 'underline', 'clear',
                    'strikethrough', 'superscript', 'subscript'
                ]
            ],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['height', ['height']]
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
        'attachment_absolute_uri': True,
        'attachment_require_authentication': True,
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            'theme': 'monokai',
        },
    },
}

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs/logs.log"),
                "when": "D",
                "interval": 1,
                "backupCount": 100,
            }
        },
        "loggers": {
            "django": {"handlers": ["file"], "level": "INFO", "propagate": True},
            "project": {"handlers": ["file"], "level": "INFO", "propagate": True},
            "": {"handlers": ["file"], "level": "INFO", "propagate": True},
        },
    }

# Configure as cache backend
# https://pypi.org/project/django-redis/

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100, "retry_on_timeout": True
            }
        }
    }
}

DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
