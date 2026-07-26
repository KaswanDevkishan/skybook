"""Django settings for SkyBook."""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def environment_bool(name, *, default=False):
    """Read a strict boolean from the environment."""
    value = os.environ.get(name)
    if value is None:
        return default

    normalized_value = value.strip().lower()
    if normalized_value in {"1", "true", "yes", "on"}:
        return True
    if normalized_value in {"0", "false", "no", "off"}:
        return False
    raise ImproperlyConfigured(f"{name} must be a boolean value.")


def environment_list(name, *, default=()):
    """Read a comma-separated list and discard empty entries."""
    value = os.environ.get(name)
    if value is None:
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


def environment_int(name, *, default):
    """Read a non-negative integer from the environment."""
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        parsed_value = int(value)
    except ValueError as error:
        raise ImproperlyConfigured(f"{name} must be a non-negative integer.") from error
    if parsed_value < 0:
        raise ImproperlyConfigured(f"{name} must be a non-negative integer.")
    return parsed_value


IS_RENDER = environment_bool("RENDER")
DEBUG = environment_bool("DEBUG")

SECRET_KEY = os.environ.get("SECRET_KEY")
if IS_RENDER and not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY is required when running on Render.")
if IS_RENDER and DEBUG:
    raise ImproperlyConfigured("DEBUG must be false when running on Render.")
if not SECRET_KEY:
    SECRET_KEY = "django-insecure-skybook-development-only"

render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
local_hosts = ("localhost", "127.0.0.1", "[::1]")
default_allowed_hosts = (
    (render_hostname,) if IS_RENDER and render_hostname else (() if IS_RENDER else local_hosts)
)
ALLOWED_HOSTS = environment_list("ALLOWED_HOSTS", default=default_allowed_hosts)
if IS_RENDER and not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "RENDER_EXTERNAL_HOSTNAME or a non-empty ALLOWED_HOSTS value is required "
        "when running on Render."
    )

local_csrf_origins = ("http://localhost:8000", "http://127.0.0.1:8000")
default_csrf_origins = (
    (f"https://{render_hostname}",)
    if IS_RENDER and render_hostname
    else (() if IS_RENDER else local_csrf_origins)
)
CSRF_TRUSTED_ORIGINS = environment_list(
    "CSRF_TRUSTED_ORIGINS",
    default=default_csrf_origins,
)
if IS_RENDER and not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured(
        "A non-empty CSRF_TRUSTED_ORIGINS value is required when "
        "RENDER_EXTERNAL_HOSTNAME is unavailable on Render."
    )


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "reservations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "skybook.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "skybook.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("DJANGO_DB_PATH", BASE_DIR / "db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if IS_RENDER
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

if IS_RENDER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = environment_int("SECURE_HSTS_SECONDS", default=3600)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "reservations:sign_in"
LOGIN_REDIRECT_URL = "reservations:account"
