"""
Django settings for Baches_Web project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from django.contrib.messages import constants as messages
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "8)n^)ae)@syt+3pk*l8a30_tjf4ox@c$^c*@j(ind1muv!zzkx"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#  DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #  GIS
    "django.contrib.gis",
    #  MY APPS
    "app_accounts",
    "app_admin",
    "app_api",
    "app_public",
    "app_contributors",
    "app_db",
    #  3 PARTY APPS
    "crispy_forms",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    # TEST
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # <=================================>#
    #            Custom					#
    # <=================================>#
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # CORS
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "Baches_Web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Base
            os.path.join(BASE_DIR, "template_base"),
            # Public Templates
            os.path.join(BASE_DIR, "app_public", "public_templates"),
            # Account Templates
            os.path.join(BASE_DIR, "app_accounts", "account_templates"),
            # Admin Templates
            os.path.join(BASE_DIR, "app_admin", "admin_templates"),
            # Contributors Templates
            os.path.join(BASE_DIR, "app_contributors", "contrib_templates"),
            # API
            os.path.join(BASE_DIR, "app_api", "api_templates"),
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

WSGI_APPLICATION = "Baches_Web.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "es-ar"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
PROJECT_ROOT = os.path.join(os.path.abspath(__file__))

#  STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#  STATIC_URL = "/static/"


STATIC_ROOT = "/static/"
STATIC_URL = "/static/"


STATICFILES_DIRS = (
    # os.path.join(PROJECT_ROOT, 'static'),
    # Public
    # os.path.join(PROJECT_ROOT, 'app_public', 'static'),
    os.path.join(BASE_DIR, "static"),
    # Public
    os.path.join(BASE_DIR, "app_public", "static"),
    # Accounts
    os.path.join(BASE_DIR, "app_accounts", "static"),
    # Admin
    os.path.join(BASE_DIR, "app_admin", "static"),
    #  Contributor
    os.path.join(BASE_DIR, "app_contributors", "static"),
)


#  CUSTOM CONFIG
#  STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AUTH_USER_MODEL = "app_db.User"


# Custom Django auth settings
LOGIN_URL = "accounts_ingresar"
LOGOUT_URL = "accounts_salir"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
# Messages built-in framework
MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
# Third party apps configuration
CRISPY_TEMPLATE_PACK = "bootstrap3"
# Session time
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60  #


#  REST FRAMEWORK
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}


# LOCAL
# GEO DANGO
if os.name == "nt":
    import platform

    OSGEO4W = r"C:\OSGeo4W"
    if "64" in platform.architecture()[0]:
        OSGEO4W += "64"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ["OSGEO4W_ROOT"] = OSGEO4W
    os.environ["GDAL_DATA"] = OSGEO4W + r"\share\gdal"
    os.environ["PROJ_LIB"] = OSGEO4W + r"\share\proj"
    os.environ["PATH"] = OSGEO4W + r"\bin;" + os.environ["PATH"]


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("POSTGRES_ENGINE"),
        "NAME": os.environ.get("POSTGRES_DB", "db.sqlite3"),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5433"),
    },
}


if os.getenv("DYNO"):
    GDAL_LIBRARY_PATH = os.path.expandvars(os.getenv("GDAL_LIBRARY_PATH"))
    GEOS_LIBRARY_PATH = os.path.expandvars(os.getenv("GEOS_LIBRARY_PATH"))
    DATABASES["default"] = dj_database_url.parse(
        os.getenv("DATABASE_URL"), "django.contrib.gis.db.backends.postgis"
    )


GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH")


#  CORS CONFIG
CORS_ORIGIN_ALLOW_ALL = (
    True  # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
)
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = [
# 'http://localhost:3030',
# ] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
# CORS_ORIGIN_REGEX_WHITELIST = [
# 'http://localhost:3030',
# ]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}


# GRAPHVIZ
GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}