"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    print("WARNING: No SECRET_KEY envvar found! A public one will be used.")
    SECRET_KEY = "1n!p*xwg$-%h$*_fxe+iu56m)nt-29#&d^l!l"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "reservations",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cuser",
    "django_registration",
    "bootstrap4",
    "rooms",
    "profiles",
    "django_extensions",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["global_templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "website.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

print("If no valid config is found, then it'll default to SQLite...")
DB_HOST = os.getenv("DB_HOST")
if DB_HOST is not None:
    db = {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": DB_HOST,
    }
    if not all(db.values()):
        print("No complete DB configuration found. Defaulting to SQLite.")
        invalid = [
            k for k in ("HOST", "NAME", "USER", "ENGINE", "PASSWORD") if db[k] is None
        ]
        print("\tInvalid value for key: " + ", ".join(invalid))
    else:  # Valid config items found
        print(
            "\tDB configuration found:"
            + str({k: db[k] for k in ("HOST", "NAME", "USER")})
        )
        DATABASES["default"] = db

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# https://django-registration.readthedocs.io/en/3.0/quickstart.html

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window

AUTH_USER_MODEL = "cuser.CUser"

ADMINS = [("Admin", "santacatalinareservas@gmail.com")]
SERVER_EMAIL = "No contestar <santacatalinareservas+no-contestar@gmail.com>"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

username = os.environ.get("DJANGO_MAIL_HOST_USER", None)
password = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", None)

if not (username and password):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    print("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
else:
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = username
    EMAIL_HOST_PASSWORD = password
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = "No contestar <santacatalinareservas@gmail.com>"
    EMAIL_SUBJECT_PREFIX = "[Reservas Santa] "

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django": {"handlers": ["console"], "propagate": True},
        "reservations": {"level": "DEBUG", "handlers": ["console"], "propagate": True},
    },
}

#
# Turns computation settings
#

INITIAL_YEAR_COUNT = 2020  # Year corresponding to the following turns configuration
"""2020
Elvira :  9 al 16 de enero
María Antonia 17 al 24 de enero
Marcela 25 al 1 de febrero
Carlos 2 al 10 de febrero
Daniel 11 al 18 de febrero
Jacinto 19 al 26 de febrero
Calixto 1 al 8 de enero
"""

# Production DB IDs of the Users. The order is relevant!
TURN_RESPONSIBLES = {
    "Elvira": 3,  # Elvira
    "María Antonia": 13,  # Gonzalo
    "Marcela": 6,  # Marcela
    "Carlos": 30,  # Adriana
    "Daniel": 35,  # María
    "Jacinto": 18,  # Jacinto
    "Calixto": 4,  # Ana
}


try:
    from .local_settings import *
except ImportError:
    pass
