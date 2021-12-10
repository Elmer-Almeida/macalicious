import os

import django_heroku
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)4l*^n-uu2f&5y^8qdkxo5wp9t4vlwd-b*t4j-1sh8+-y1@tq5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',

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
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

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
                'cart.context_processors.cart_information'
            ],
        },
    },
]

WSGI_APPLICATION = 'macalicious.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# HEROKU: uncomment for deployment
# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'd9oaqgr4p1u9f5',
#             'USER': 'xhjfdfmpcuitpj',
#             'PASSWORD': '910c838cdd4d647658f93d74b028af93069968153f750732675f3e8a913f74c0',
#             'HOST': 'ec2-34-193-235-32.compute-1.amazonaws.com',
#             'PORT': '5432',
#         }
#     }


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

# Email settings
DEFAULT_FROM_EMAIL = "Macalicious <shop.macalicious@gmail.com>"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "shop.macalicious@gmail.com"
EMAIL_HOST_PASSWORD = "Canada2009!!!"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Google Settings (reCaptcha)
GOOGLE_RECAPTCHA_SITE_KEY = '6LeJ8JIdAAAAAK2_J_1hWKxe19d34fUGkykJuEh8'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LeJ8JIdAAAAAAphAm0MmXKaq7LSsYe7u7odT7Iw'

# Local sqlite3 database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9oaqgr4p1u9f5',
        'USER': 'xhjfdfmpcuitpj',
        'PASSWORD': '910c838cdd4d647658f93d74b028af93069968153f750732675f3e8a913f74c0',
        'HOST': 'ec2-34-193-235-32.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# Activate Django-Heroku.
if not DEBUG:
    django_heroku.settings(locals())

# AWS settings
# HEROKU: uncomment for deployment
AWS_S3_HOST = 's3.ca-central-1.amazonaws.com'
AWS_ACCESS_KEY_ID = "AKIA6CLFKBXF6LGUHXVZ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "printlineinc-bucket"
AWS_S3_REGION_NAME = 'ca-central-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_ENCRYPTION = True
AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_S3_SIGNATURE_VERSION = 's3v4'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
