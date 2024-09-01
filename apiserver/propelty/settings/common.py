# Python imports
import os
import ssl
from urllib.parse import urlparse

import certifi

# Third party imports
import dj_database_url

# Django imports
from django.core.management.utils import get_random_secret_key
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from corsheaders.defaults import default_headers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret Key
SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", "0"))

# Allowed Hosts
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # Third-party things
    "rest_framework",
    "corsheaders",
    "django_celery_beat",
    "storages",
    # Inhouse apps
    # "propelty.analytics",
    # "propelty.app",
    # "propelty.space",
    # "propelty.bgtasks",
    "propelty.db",
    # "propelty.utils",
    # "propelty.web",
    # "propelty.middleware",
    # "propelty.license",
    # "propelty.api",
    # "propelty.authentication",
]

# Middlewares
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # "propelty.authentication.middleware.session.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "crum.CurrentRequestUserMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    # "propelty.middleware.api_log_middleware.APITokenLogMiddleware",
]

# Rest Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    # "EXCEPTION_HANDLER": "propelty.authentication.adapter.exception.auth_exception_handler",
}

# Django Auth Backend
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)  # default

# Root Urls
ROOT_URLCONF = "propelty.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# CORS Settings
CORS_ALLOW_CREDENTIALS = True
cors_origins_raw = os.environ.get("CORS_ALLOWED_ORIGINS", "")
# filter out empty strings
cors_allowed_origins = [
    origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()
]
if cors_allowed_origins:
    CORS_ALLOWED_ORIGINS = cors_allowed_origins
    secure_origins = (
        False
        if [origin for origin in cors_allowed_origins if "http:" in origin]
        else True
    )
else:
    CORS_ALLOW_ALL_ORIGINS = True
    secure_origins = False

CORS_ALLOW_HEADERS = [*default_headers, "X-API-Key"]

# Application Settings
WSGI_APPLICATION = "propelty.wsgi.application"
ASGI_APPLICATION = "propelty.asgi.application"

# Django Sites
SITE_ID = 1

# User Model
# AUTH_USER_MODEL = "db.User"

# Database
if bool(os.environ.get("DATABASE_URL")):
    # Parse database configuration from $DATABASE_URL
    DATABASES = {
        "default": dj_database_url.config(),
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

# Redis Config
REDIS_URL = os.environ.get("REDIS_URL")
REDIS_SSL = REDIS_URL and "rediss" in REDIS_URL

if REDIS_SSL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": False},
            },
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

# Password validations
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Password reset time the number of seconds the uniquely generated uid will be valid
PASSWORD_RESET_TIMEOUT = 3600

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static-assets", "collected-static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Media Settings
MEDIA_ROOT = "mediafiles"
MEDIA_URL = "/media/"

# Internationalization
LANGUAGE_CODE = "ru-ru"
USE_I18N = True
USE_L10N = True

# Timezones
USE_TZ = True
TIME_ZONE = "UTC"

# Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Storage Settings
# Use Minio settings
USE_MINIO = int(os.environ.get("USE_MINIO", 0)) == 1

if REDIS_SSL:
    redis_url = os.environ.get("REDIS_URL")
    broker_url = f"{redis_url}?ssl_cert_reqs={ssl.CERT_NONE.name}&ssl_ca_certs={certifi.where()}"
    CELERY_BROKER_URL = broker_url
else:
    CELERY_BROKER_URL = REDIS_URL

CELERY_IMPORTS = (
    # scheduled tasks
    "propelty.bgtasks.issue_automation_task",
    "propelty.bgtasks.exporter_expired_task",
    "propelty.bgtasks.file_asset_task",
    "propelty.bgtasks.email_notification_task",
    "propelty.bgtasks.api_logs_task",
    # management tasks
    "propelty.bgtasks.dummy_data_task",
)

FILE_SIZE_LIMIT = int(os.environ.get("FILE_SIZE_LIMIT", 5242880))

# Skip environment variable configuration
SKIP_ENV_VAR = os.environ.get("SKIP_ENV_VAR", "1") == "1"

DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get("FILE_SIZE_LIMIT", 5242880))

# Cookie Settings
SESSION_COOKIE_SECURE = secure_origins
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = "propelty.db.models.session"
SESSION_COOKIE_AGE = os.environ.get("SESSION_COOKIE_AGE", 604800)
SESSION_COOKIE_NAME = "propelty-session-id"
SESSION_COOKIE_DOMAIN = os.environ.get("COOKIE_DOMAIN", None)
SESSION_SAVE_EVERY_REQUEST = (
    os.environ.get("SESSION_SAVE_EVERY_REQUEST", "0") == "1"
)

# Admin Cookie
ADMIN_SESSION_COOKIE_NAME = "propelty-admin-session-id"
ADMIN_SESSION_COOKIE_AGE = os.environ.get("ADMIN_SESSION_COOKIE_AGE", 3600)

# CSRF cookies
CSRF_COOKIE_SECURE = secure_origins
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = cors_allowed_origins
CSRF_COOKIE_DOMAIN = os.environ.get("COOKIE_DOMAIN", None)
# CSRF_FAILURE_VIEW = "propelty.authentication.views.common.csrf_failure"

# Base URLs
ADMIN_BASE_URL = os.environ.get("ADMIN_BASE_URL", None)
SPACE_BASE_URL = os.environ.get("SPACE_BASE_URL", None)
APP_BASE_URL = os.environ.get("APP_BASE_URL")

HARD_DELETE_AFTER_DAYS = int(os.environ.get("HARD_DELETE_AFTER_DAYS", 60))