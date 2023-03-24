"""
Django settings for bulletin project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure-4hme%^1^jeh1f_+$(4$ao$ci9jsj=$@z#an6up%5x2s6$_st$_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", 'true').lower() == 'true')

ALLOWED_HOSTS = ["localhost",
                 "127.0.0.1",
                 "0.0.0.0",
                 os.environ.get("ALLOWED_URL", "0.0.0.0")]

CSRF_TRUSTED_ORIGINS = ['https://*.withnoedge.tech', os.environ.get("ALLOWED_CSRF", "http://127.0.0.1")]

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

# Application definition
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'daphne',
    'channels',
    'django_celery_beat',
    'apps.home.config.HomeConfig',
    'apps.system.config.SystemConfig',
    'apps.internet_speedtester.config.InternetSpeedtesterConfig',
    'apps.weather.config.WeatherConfig',
    'apps.social.config.SocialConfig',
]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py

# Fixtures DIR
FIXTURE_DIRS = [os.path.join(BASE_DIR, 'core/fixtures')]

TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

# WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        ### Method 1: Via local Redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #      "hosts": [('127.0.0.1', 6379)],
        # },

        ### Method 2: Via In-memory channel layer
        ## Using this method.
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DB_FROM_ENV = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(DB_FROM_ENV)

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Africa/Cairo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Social/Twitter Access Token Variables
TWT_BEARER_TOKEN = os.environ.get("TWT_BEARER_TOKEN", "")
TWT_CONSUMER_KEY = os.environ.get("TWT_CONSUMER_KEY", "")
TWT_CONSUMER_SECRET = os.environ.get("TWT_CONSUMER_SECRET", "")
TWT_ACCESS_KEY = os.environ.get("TWT_ACCESS_KEY", "")
TWT_ACCESS_SECRET = os.environ.get("TWT_ACCESS_SECRET", "")

# Social/Slack Access Token Variables
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_BOT_CHANNEL = os.environ.get("SLACK_BOT_CHANNEL", "")

# Tasks Interval Timing
SPEEDTESTER_INTERVAL_TIME_HRS = os.environ.get("SPEEDTESTER_INTERVAL_TIME_HRS", 4)
TEXT_TWEET_INTERVAL_TIME_MINS = os.environ.get("TEXT_TWEET_INTERVAL_TIME_MINS", 60)
IMAGE_TWEET_INTERVAL_TIME_DAYS = os.environ.get("IMAGE_TWEET_INTERVAL_TIME_DAYS", 1)

# Redis Configuration Options
REDIS_SERVER_HOST = os.environ.get("REDIS_SERVER_HOST", 'localhost')
REDIS_SERVER_PORT = os.environ.get("REDIS_SERVER_PORT", 6379)

# Celery Configuration Options
CELERY_TIMEZONE = "Africa/Cairo"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_URL = f'redis://{REDIS_SERVER_HOST}:{REDIS_SERVER_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_SERVER_HOST}:{REDIS_SERVER_PORT}/0'
CELERY_BACKEND_URL = f'redis://{REDIS_SERVER_HOST}:{REDIS_SERVER_PORT}/0'
