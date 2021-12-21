import os
from pathlib import Path

import django_heroku
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)4l*^n-uu2f&5y^8qdkxo5wp9t4vlwd-b*t4j-1sh8+-y1@tq5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Initialize env variables
env = environ.Env()
environ.Env.read_env()

ALLOWED_HOSTS = [
    "macalicious.herokuapp.com",
    "www.macalicious.ca",
    "localhost"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'whitenoise.runserver_nostatic',

    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",
    'registration',  # django-registration-redux
    'phonenumber_field',

    # Project apps
    'account',
    'cart',
    'contact',
    'newsletter',
    'orders',
    'search',
    'shop'
]

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'macalicious.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_information',
                'newsletter.context_processors.newsletter_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'macalicious.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static/static_dirs')
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static/static_root')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Crispy forms - bootstrap 5
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django registration redux settings
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True

# # Debug Mode: Email Provider
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/shop/'

# Phone numbers field
PHONENUMBER_DEFAULT_REGION = 'CA'

if DEBUG:
    # Google reCAPTCHA keys - use local env variables
    GOOGLE_RECAPTCHA_SITE_KEY = env('GOOGLE_RECAPTCHA_SITE_KEY')
    GOOGLE_RECAPTCHA_SECRET_KEY = env('GOOGLE_RECAPTCHA_SECRET_KEY')

    DEBUG_EMAIL = True

    if DEBUG_EMAIL:
        EMAIL_HOST_USER = env('EMAIL_HOST_USER')
        DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
        EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
        EMAIL_USE_TLS = env('EMAIL_USE_TLS')
        EMAIL_PORT = env('EMAIL_PORT')
        EMAIL_HOST = env('EMAIL_HOST')
    else:
        EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Google reCAPTCHA keys - use heroku env variable
    GOOGLE_RECAPTCHA_SITE_KEY = os.environ['GOOGLE_RECAPTCHA_SITE_KEY']
    GOOGLE_RECAPTCHA_SECRET_KEY = os.environ['GOOGLE_RECAPTCHA_SECRET_KEY']

    # Email settings
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
    EMAIL_PORT = os.environ['EMAIL_PORT']
    EMAIL_HOST = os.environ['EMAIL_HOST']

    ADMINS = [('Elmer Almeida', 'elmer.dev.95@gmail.com'), ]

    # AWS settings
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_HOST = os.environ['AWS_S3_HOST']
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_ENCRYPTION = True
    AWS_S3_ADDRESSING_STYLE = "virtual"
    AWS_S3_SIGNATURE_VERSION = 's3v4'

    # activate django-heroku
    django_heroku.settings(locals())

    # always use HTTPS
    SECURE_SSL_REDIRECT = True

    # Database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DATABASE_NAME'],
            'USER': os.environ['DATABASE_USER'],
            'PASSWORD': os.environ['DATABASE_PASSWORD'],
            'HOST': os.environ['DATABASE_HOST'],
            'PORT': os.environ['DATABASE_PORT']
        }
    }

