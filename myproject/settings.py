import os
import logging
from pathlib import Path
from datetime import timedelta
import django
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

# Basic runtime info (temporary; safe: logs presence, not values)
logging.getLogger(__name__).error(
    "ENV CHECK: DJANGO_SETTINGS_MODULE=%s, SECRET_KEY present=%s, FRONTEND_SECRET_KEY present=%s, ESP_SECRET_KEY present=%s, DEBUG=%s",
    os.environ.get("DJANGO_SETTINGS_MODULE"),
    bool(os.getenv("SECRET_KEY")),
    bool(os.getenv("FRONTEND_SECRET_KEY")),
    bool(os.getenv("ESP_SECRET_KEY")),
    os.getenv("DEBUG"),
)

print("DJANGO VERSION:", django.get_version())

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY must come from environment in production
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")

# Secrets used by your app (application-level)
ESP_SECRET_KEY = os.getenv("ESP_SECRET_KEY")
FRONTEND_SECRET_KEY = os.getenv("FRONTEND_SECRET_KEY")

# Debug flag (string "True" -> True)
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Hosts
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",") if os.environ.get("ALLOWED_HOSTS") else ["*"]

# Database (Render DATABASE_URL or fallback to sqlite)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")
    )
}

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api",
    "corsheaders",
]

# Middleware (exception logger first for debugging; remove after fix)
MIDDLEWARE = [
    "api.middleware.ExceptionLoggingMiddleware",  # temporary: logs full tracebacks to stderr
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "myproject.wsgi.application"

# REST framework minimal config
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://iot-pwa.vercel.app",
    "https://pwa.flowofthings.net",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security-related defaults (adjust for production)
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging: ensure exception_logger writes to stderr so Render/Gunicorn capture it
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "stream": "ext://sys.stderr"},
    },
    "loggers": {
        "exception_logger": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}

# Any other app-specific settings (JWT lifetimes, etc.) can go here
# Example placeholder (unused unless you add JWT logic)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}