import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ SECRET_KEY from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# ✅ Root URL configuration
ROOT_URLCONF = 'myproject.urls'

# ✅ Debug off in production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ✅ Allow all hosts during testing, restrict later
ALLOWED_HOSTS = ['*']  # change to ['django-iot-backend.onrender.com'] after testing

# ✅ Database configuration using Render Postgres or fallback SQLite
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR}/db.sqlite3')
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

# ✅ Middleware (required for admin, sessions, auth, messages)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # required
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # required
    'django.contrib.messages.middleware.MessageMiddleware',    # required
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Templates (required for admin and DRF browsable API)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ✅ Static files (Render needs this)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')