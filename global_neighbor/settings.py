import os
from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")
CMS_CONFIRM_VERSION4 = True
SITE_ID = 1
BLUESKY_USERNAME = config("BLUESKY_USERNAME")
BLUESKY_PASSWORD = config("BLUESKY_PASSWORD")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)
print("DEBUG is", DEBUG)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
EMAIL_FILE_PATH = config("EMAIL_FILE_PATH")
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_extensions",
    "global_neighbor.apps.GlobalNeighborConfig",
    "blog",
    "neighborhood",
    "taggit",
    "cms",
    "menus",
    "treebeard",
    "sekizai",
    "djangocms_text_ckeditor",
    "filer",
    "easy_thumbnails",
    "rest_framework",
    "rest_framework.authtoken",
]

AUTH_USER_MODEL = "global_neighbor.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "global_neighbor.middleware.BlockPostingMiddleware",
]

ROOT_URLCONF = "global_neighbor.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "global_neighbor/templates"),
            os.path.join(BASE_DIR, "blog/templates"),
            os.path.join(BASE_DIR, "neighborhood/templates"),
        ],  # ✅ Ensure templates are recognized
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

WSGI_APPLICATION = "global_neighbor.wsgi.application"
# ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
if DEBUG is True:
    db_engine = "django.db.backends.postgresql"
    options = {}
else:
    db_engine = "django.db.backends.mysql"
    options = (
        {
            "charset": "utf8mb4",
        },
    )


DATABASES = {
    "default": {
        "ENGINE": db_engine,
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
        "CONN_MAX_AGE": 60,  # Reuse connections for 60 seconds
        "OPTIONS": options,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "global_neighbor" / "static",
    BASE_DIR / "blog" / "static",
    BASE_DIR / "neighborhood" / "static",
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Ensure this exists

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# For PythonAnywhere
STATICFILES_DIRS = [
    os.path.join(
        BASE_DIR, "global_neighbor/static"
    ),  # If you have a local static folder
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
