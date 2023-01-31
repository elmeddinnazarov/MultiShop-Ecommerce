"""
Django settings for MultiShop project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from os import getenv #to get enviroment files
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG') == 'True'

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS').split(', ') # list halinda olduguna gore split edilir 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps', # en sonda sitemap yaradildiqda elave olunur
    
    #INTERNALS
    'ecommerce',
    'customer',
    
    # EXTERNALS
    'django_cleanup.apps.CleanupConfig', #bu app eleva olunduqda şekiller admin panelden silindiyi zaman sayttan ve s3 den silinir
    'storages', # xarici storage serverlernen ';lemek ucundur
    'ckeditor', # daha selqeli html yazilari ucun istifade olunur
    'imagekit', # yuklenen sekilleri standart olcuye cevirir
    'django_filters' # tarixe, qiymete vs.. filtireleme ucun istifade olunur
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MultiShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'MultiShop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT'),
    }
}


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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('az', _('Azərbaycanca')),
    ('tr', _('Türkce')),
    ('en', _('English'))
]

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'staticfiles/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]

STATICFILES_FINDERS = [ # static folerini avtomatiok tapsin deye elave olunur
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



############################### AWS-S3 #######################
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ACCESS_KEY_ID = getenv('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = getenv('AWS_S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = getenv('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = getenv('AWS_DEFAULT_ACL')
AWS_QUERYSTRING_AUTH = getenv('AWS_QUERYSTRING_AUTH') == 'True'
AWS_S3_REGION_NAME = getenv('AWS_S3_REGION_NAME')
AWS_LOCATION = 'media'


AWS_S3_CUSTOM_DOMAIN = '{}.s3.{}.amazonaws.com'.format(
    AWS_STORAGE_BUCKET_NAME,
    AWS_S3_REGION_NAME
)

# MEDIA_URL = 'https:/{}/{}/'.format(
#     AWS_S3_CUSTOM_DOMAIN,
#     AWS_LOCATION
# )

############################### AWS-S3 #######################


LOGIN_URL = 'customer:login' # login_requiered icinde herdefe yazmamaq ucun burada default olaraq yazilir

EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = int(getenv('EMAIL_PORT'))
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True




SECURE_HSTS_SECONDS = int(getenv('SECURE_HSTS_SECONDS'))
SECURE_HSTS_SECONDS = getenv('SECURE_HSTS_SECONDS') == 'True'
SECURE_HSTS_INCLUDE_SUBDOMAINS = getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS') == 'True'
SECURE_SSL_REDIRECT = getenv('SECURE_SSL_REDIRECT') == 'True'
SESSION_COOKIE_SECURE = getenv('SESSION_COOKIE_SECURE') == 'True'
CSRF_COOKIE_SECURE = getenv('CSRF_COOKIE_SECURE') == 'True'