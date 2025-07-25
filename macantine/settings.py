"""
Django settings for macantine project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import logging
import os
import sys
from pathlib import Path

import dotenv  # noqa
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from macantine.sentry import before_send

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET")
SECURE_SSL_REDIRECT = os.getenv("FORCE_HTTPS") == "True"

# The site uses http or https?
SECURE = os.getenv("SECURE") == "True"
PROTOCOL = "https" if SECURE else "http"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"
# Default to True so that tests can pass without this env var being defined
DEBUG_FRONT = os.getenv("DEBUG_FRONT") == "True" if os.getenv("DEBUG_FRONT") else True
AUTH_USER_MODEL = "data.User"
AUTHENTICATION_BACKENDS = [
    "macantine.backends.EmailUsernameBackend",
]
ALLOWED_HOSTS = [x.strip() for x in os.getenv("ALLOWED_HOSTS").split(",")]
ENFORCE_HOST = os.getenv("ENFORCE_HOST", None)

DEBUG_PERFORMANCE = os.getenv("DEBUG") == "True" and os.getenv("DEBUG_PERFORMANCE") == "True"

# Environment

ENVIRONMENT = os.getenv("ENVIRONMENT")


# Sentry
# No need making this one secret: https://forum.sentry.io/t/dsn-private-public/6297/3
if not DEBUG:
    sentry_sdk.init(
        dsn="https://db78f7d440094c498a02135e8abefa27@sentry.incubateur.net/2",
        integrations=[DjangoIntegration(), CeleryIntegration()],
        # Tracing: set traces_sample_rate to 1.0 to capture 100% of transactions
        traces_sample_rate=0.2,  # 20%
        # Profiling: set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        # The profiles_sample_rate setting is relative to the traces_sample_rate setting.
        profiles_sample_rate=0.2,  # 4%
        send_default_pii=False,
        send_client_reports=False,
        before_send=before_send,
    )
    sentry_sdk.set_level(logging.ERROR)

INTERNAL_IPS = []

# Application definition
WAGTAIL_INSTALLED_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.api.v2",
    "wagtail",
    "modelcluster",
    "taggit",
    "cms",
]
INSTALLED_APPS = WAGTAIL_INSTALLED_APPS + [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    "django_vite_plugin",
    "webpack_loader",
    "rest_framework",
    "oauth2_provider",
    "ckeditor",
    "ckeditor_uploader",
    "macantine",
    "data",
    "api",
    "web",
    "magicauth",
    "django_extensions",
    "django_filters",
    "django_celery_results",
    "common",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "simple_history",
]

# Storing celery results
CELERY_RESULT_EXTENDED = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "macantine.middleware.RedirectMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "csp.middleware.CSPMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]
CSRF_COOKIE_NAME = "csrftoken"
ROOT_URLCONF = "macantine.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "macantine.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.getenv("DB_USER"),
        "NAME": os.getenv("DB_NAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "CONN_MAX_AGE": 60,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"
LANGUAGES = (("fr", "Français"),)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "templates", "locale"),
]

TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True  # True is default as of Django 5

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media and file storage
default_file_storage = os.getenv("DEFAULT_FILE_STORAGE")

STORAGES = {
    "default": {
        "BACKEND": default_file_storage,
    },
    "staticfiles": {
        "BACKEND": os.getenv("STATICFILES_STORAGE"),
    },
}

if default_file_storage == "storages.backends.s3.S3Storage":
    AWS_ACCESS_KEY_ID = os.getenv("CELLAR_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("CELLAR_SECRET")
    AWS_S3_ENDPOINT_URL = os.getenv("CELLAR_HOST")
    AWS_STORAGE_BUCKET_NAME = os.getenv("CELLAR_BUCKET_NAME")
    AWS_LOCATION = "media"
    AWS_QUERYSTRING_AUTH = False

MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}

SESSION_COOKIE_AGE = 31536000
SESSION_COOKIE_SECURE = os.getenv("SECURE") == "True"
SESSION_COOKIE_HTTPONLY = True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/s-identifier"

HOSTNAME = os.getenv("HOSTNAME")

# API - Django Rest Framework

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "UPLOADED_FILES_USE_URL": True,
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "EXCEPTION_HANDLER": "api.middleware.custom_exception_handler",
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Reading doc API and load it in the swagger
with open(BASE_DIR / "docs/api.html") as f:
    doc_api = f.read()


SPECTACULAR_SETTINGS = {
    "TITLE": "Ma Cantine API",
    "DESCRIPTION": doc_api,
    "VERSION": "1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "PREPROCESSING_HOOKS": [
        "drf_spectacular.hooks.preprocess_exclude_path_format",
        "api.hooks.ma_cantine_preprocessing_hook",
    ],
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    # Oauth2 related settings. used for example by django-oauth2-toolkit.
    # https://spec.openapis.org/oas/v3.0.3#oauth-flows-object
    "OAUTH2_FLOWS": ["authorizationCode"],
    "OAUTH2_AUTHORIZATION_URL": "/o/authorize/",
    "OAUTH2_TOKEN_URL": "/o/token/",
    "OAUTH2_SCOPES": {"read": "Lecture", "write": "Ecriture"},
}

# Frontend - VueJS application

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/dist/"),
    os.path.join(BASE_DIR, "build/"),
]
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": DEBUG,
        "BUNDLE_DIR_NAME": "/bundles/",
        "STATS_FILE": os.path.join(FRONTEND_DIR, "dist/webpack-stats.json"),
    }
}

DJANGO_VITE_PLUGIN = {
    "DEV_MODE": DEBUG_FRONT,
    "BUILD_DIR": "build",
}

# Email
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")

if DEBUG and EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025

ANYMAIL = {
    "SENDINBLUE_API_KEY": os.getenv("SENDINBLUE_API_KEY", ""),
}
NEWSLETTER_SENDINBLUE_LIST_ID = os.getenv("NEWSLETTER_SENDINBLUE_LIST_ID")

# Magicauth
MAGICAUTH_EMAIL_FIELD = "email"
MAGICAUTH_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
MAGICAUTH_LOGIN_URL = "envoyer-email-conexion"
MAGICAUTH_LOGGED_IN_REDIRECT_URL_NAME = "app"
MAGICAUTH_EMAIL_SUBJECT = "Votre lien de connexion avec Ma Cantine"
MAGICAUTH_EMAIL_HTML_TEMPLATE = "magicauth/magicauth_email.html"
MAGICAUTH_EMAIL_TEXT_TEMPLATE = "magicauth/magicauth_email.txt"
MAGICAUTH_LOGIN_VIEW_TEMPLATE = "magicauth/login_magicauth.html"
MAGICAUTH_EMAIL_SENT_VIEW_TEMPLATE = "magicauth/magicauth_email_sent.html"
MAGICAUTH_ENABLE_2FA = False

# CK Editor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Format", "Blockquote"],
            ["Bold", "Italic"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
            ],
            ["Link", "Unlink"],
            [
                "Image",
                "-",
                "Table",
                "SpecialChar",
            ],
            ["Source", "Maximize"],
        ],
        "extraPlugins": ",".join(
            [
                "image2",
                "codesnippet",
                "placeholder",
            ]
        ),
        "removePlugins": ",".join(["image"]),
    }
}

# Analytics
MATOMO_ID = os.getenv("MATOMO_ID", "")

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Performance debug with Django debug console
if DEBUG_PERFORMANCE:
    INTERNAL_IPS.append("127.0.0.1")
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# Maximum CSV import file size: 10Mo
CSV_IMPORT_MAX_SIZE = 10485760
CSV_IMPORT_MAX_SIZE_PRETTY = "10Mo"

# Size of each chunk when processing files
CSV_PURCHASE_CHUNK_LINES = 10000

# CSP headers (https://content-security-policy.com/)

# CSP Debug domains -  unsafe-eval needed in DEBUG for hot-reload of the frontend server
CSP_DEBUG_DOMAINS = (
    "'unsafe-eval'",
    "localhost:*",
    "0.0.0.0:*",
    "127.0.0.1:*",
    "www.ssa.gov",  # for a11y testing with ANDI
    "ajax.googleapis.com",  # for a11y testing with ANDI
)

# CSP Default policy for resources such as JS, CSS, AJAX, etc. Note that not all directives fallback to this.
CSP_DEFAULT_SRC = ("'self'",)
if DEBUG:
    CSP_DEFAULT_SRC += CSP_DEBUG_DOMAINS

# CSP valid sources of stylesheets or CSS
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "client.crisp.chat",
    "netdna.bootstrapcdn.com",
)
if DEBUG:
    CSP_STYLE_SRC += CSP_DEBUG_DOMAINS

# CSP valid sources of Javascript
CSP_SCRIPT_SRC = (
    "'self'",
    "stats.beta.gouv.fr",
    "'unsafe-inline'",
    "client.crisp.chat",
)
if DEBUG:
    CSP_SCRIPT_SRC += CSP_DEBUG_DOMAINS

# CSP valid sources of images
CSP_IMG_SRC = (
    "'self'",
    "cellar-c2.services.clever-cloud.com",
    "voxusagers.numerique.gouv.fr",
    "'unsafe-inline'",
    "stats.beta.gouv.fr",
    "www.w3.org",
    "data:",
    "image.crisp.chat",
    "jedonnemonavis.numerique.gouv.fr",
)
if DEBUG:
    CSP_IMG_SRC += CSP_DEBUG_DOMAINS

# CSP valid sources of fonts
CSP_FONT_SRC = (
    "'self'",
    "client.crisp.chat",
)
if DEBUG:
    CSP_IMG_SRC += CSP_FONT_SRC

# CSP valid sources of AJAX, WebSockets, EventSources, etc
CSP_CONNECT_SRC = (
    "'self'",
    "stats.beta.gouv.fr",
    "ws:",
    "api-adresse.data.gouv.fr",
    "geo.api.gouv.fr",
    "client.crisp.chat",
    "wss://client.relay.crisp.chat",
    "entreprise.data.gouv.fr",
    "plateforme.adresse.data.gouv.fr",
    "raw.githubusercontent.com/betagouv/ma-cantine/",  # data/schemas/imports/
)
if DEBUG:
    CSP_CONNECT_SRC += CSP_DEBUG_DOMAINS

# CSP valid sources of plugins
CSP_OBJECT_SRC = (
    "'self'",
    "cellar-c2.services.clever-cloud.com",
)
if DEBUG:
    CSP_OBJECT_SRC += CSP_DEBUG_DOMAINS

# CSP valid sources of media (audio and video)
CSP_MEDIA_SRC = (
    "'self'",
    "cellar-c2.services.clever-cloud.com",
)
if DEBUG:
    CSP_MEDIA_SRC += CSP_DEBUG_DOMAINS

# CSP valid sources for loading frames
CSP_FRAME_SRC = (
    "'self'",
    "ma-cantine.crisp.help",
    "ma-cantine-metabase.cleverapps.io",
)
if DEBUG:
    CSP_FRAME_SRC += CSP_DEBUG_DOMAINS

# Campaign dates override
ENABLE_TELEDECLARATION = os.getenv("ENABLE_TELEDECLARATION") == "True"
TELEDECLARATION_START_DATE_OVERRIDE = os.getenv("TELEDECLARATION_START_DATE_OVERRIDE", "")
TELEDECLARATION_END_DATE_OVERRIDE = os.getenv("TELEDECLARATION_END_DATE_OVERRIDE", "")
CORRECTION_START_DATE_OVERRIDE = os.getenv("CORRECTION_START_DATE_OVERRIDE", "")
CORRECTION_END_DATE_OVERRIDE = os.getenv("CORRECTION_END_DATE_OVERRIDE", "")

# Feature flags
ENABLE_XP_RESERVATION = os.getenv("ENABLE_XP_RESERVATION") == "True"
ENABLE_XP_VEGE = os.getenv("ENABLE_XP_VEGE") == "True"
ENABLE_DASHBOARD = os.getenv("ENABLE_DASHBOARD") == "True"
ENABLE_VUE3 = os.getenv("ENABLE_VUE3") == "True"
ENABLE_WASTE_MEASUREMENTS = os.getenv("ENABLE_WASTE_MEASUREMENTS") == "True"
SHOW_MANAGEMENT_INFORMATION_BANNER = os.getenv("SHOW_MANAGEMENT_INFORMATION_BANNER") == "True"

# Custom testing
TEST_RUNNER = "macantine.testrunner.MaCantineTestRunner"
OVERRIDE_TEST_SEED = os.getenv("OVERRIDE_TEST_SEED", None)

# Automatic emails
TEMPLATE_ID_NO_CANTEEN_FIRST = (
    int(os.getenv("TEMPLATE_ID_NO_CANTEEN_FIRST")) if os.getenv("TEMPLATE_ID_NO_CANTEEN_FIRST", None) else None
)
TEMPLATE_ID_NO_CANTEEN_SECOND = (
    int(os.getenv("TEMPLATE_ID_NO_CANTEEN_SECOND")) if os.getenv("TEMPLATE_ID_NO_CANTEEN_SECOND", None) else None
)
TEMPLATE_ID_NO_DIAGNOSTIC_FIRST = (
    int(os.getenv("TEMPLATE_ID_NO_DIAGNOSTIC_FIRST")) if os.getenv("TEMPLATE_ID_NO_DIAGNOSTIC_FIRST", None) else None
)

OAUTH2_PROVIDER = {
    "PKCE_REQUIRED": False,
    "SCOPES": {
        "user:read": "Lire votre profil utilisateur",
        "canteen:read": "Lire les données de votre cantine",
        "canteen:write": "Modifier les données de votre cantine",
    },
}

REDIS_URL = os.getenv("REDIS_URL")
REDIS_PREPEND_KEY = os.getenv("REDIS_PREPEND_KEY", "")

AUTHLIB_OAUTH_CLIENTS = {
    "moncomptepro": {
        "client_id": os.getenv("MONCOMPTEPRO_CLIENT_ID"),
        "client_secret": os.getenv("MONCOMPTEPRO_SECRET"),
    }
}
MONCOMPTEPRO_CONFIG = os.getenv("MONCOMPTEPRO_CONFIG")
USES_MONCOMPTEPRO = (
    os.getenv("MONCOMPTEPRO_CLIENT_ID") and os.getenv("MONCOMPTEPRO_SECRET") and os.getenv("MONCOMPTEPRO_CONFIG")
)
MAX_DAYS_HISTORICAL_RECORDS = (
    int(os.getenv("MAX_DAYS_HISTORICAL_RECORDS")) if os.getenv("MAX_DAYS_HISTORICAL_RECORDS", None) else None
)

# Wagtail CMS
WAGTAIL_SITE_NAME = "ma-cantine"
# WAGTAILADMIN_BASE_URL # Declare if null URL in notification emails
WAGTAILDOCS_EXTENSIONS = ["csv", "docx", "key", "odt", "pdf", "pptx", "rtf", "txt", "xlsx", "zip"]
