# core.production.py

import os
from core.settings import * # noqa

# SECURITY WARNING: don't run with debug turned on in production

PREPEND_WWW = True
DEBUG = TEMPLATE_DEBUG = False

# https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts

ALLOWED_HOSTS = [
    '*.valereobei.com',
    'valereobei.com',
    'www.valereobei.com'
]

# https://docs.djangoproject.com/fr/4.0/ref/settings/
# Let's Encrypt ssl/tls https

SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CSRF_USE_SESSIONS = True
CSRF_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
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
