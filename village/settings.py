"""Django settings for the village project.

This configuration is intentionally simple and heavily commented so that new
contributors can understand and extend it easily.  The project uses SQLite by
default which keeps the app self‑contained and friendly to open‑source
contributors, but any other database supported by Django can be configured
here.
"""
from pathlib import Path
import os
import base64
import hashlib

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-secret-key-change-me'

# Derive a key for encrypting private data
FERNET_KEY = base64.urlsafe_b64encode(hashlib.sha256(SECRET_KEY.encode()).digest())

DEBUG = True

ALLOWED_HOSTS: list[str] = []

# Default categories for neighborhood help offers. Villages can adjust this
# list to match local needs.
OFFER_CATEGORIES = [
    ("shopping", "Einkaufen"),
    ("tools", "Werkzeugverleih"),
    ("ride", "Fahrdienst"),
    ("care", "Pflege"),
    ("pets", "Haustiere"),
    ("garden", "Gartenhilfe"),
    ("plants", "Blumengießen"),
    ("other", "Sonstiges"),
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
if os.getenv('USE_SQLITE', '1') != '1':
    INSTALLED_APPS.append('django.contrib.gis')
INSTALLED_APPS += [
    'channels',  # WebSocket support
    'chat',  # Our chat app providing the core features
    'offers',  # Help offers with map
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'village.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates directory
        'APP_DIRS': True,  # Also look for templates inside installed apps
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

ASGI_APPLICATION = 'village.asgi.application'
WSGI_APPLICATION = 'village.wsgi.application'

if os.getenv('USE_SQLITE', '1') == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DATABASE', 'village'),
            'USER': os.getenv('MYSQL_USER', 'village'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD', 'village'),
            'HOST': os.getenv('MYSQL_HOST', 'localhost'),
            'PORT': os.getenv('MYSQL_PORT', '3306'),
        },
        'geodata': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': os.getenv('POSTGRES_DB', 'village_geo'),
            'USER': os.getenv('POSTGRES_USER', 'village'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'village'),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        },
    }
    DATABASE_ROUTERS = ['village.dbrouters.GeodataRouter']

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
