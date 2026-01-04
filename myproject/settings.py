import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ SECRET_KEY from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# ✅ Debug off in production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ✅ Allow all hosts during testing, restrict later
ALLOWED_HOSTS = ['*']  # change to ['iot-backend.onrender.com'] after testing

# ✅ Database configuration using Render Postgres
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# ✅ Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
]

# ✅ Static files (Render needs this)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')