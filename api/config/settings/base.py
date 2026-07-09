 
from pathlib import Path
from loguru import logger

from dotenv import load_dotenv
from os import path, getenv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "core_apps"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


local_env_file = path.join(BASE_DIR, ".envs", ".envs.local")
if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    "django.contrib.humanize"
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_spectacular",
    "djoser",
    "cloudinary",
    "django_filters",
    "djcelery_email",
    "django_celery_beat"
]


LOCAL_APPS = [
    "core_apps.common",
    "core_apps.user_auth",
    "core_apps.user_profile",
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core_apps.user_auth.middleware.CustomHeaderMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': getenv('POSTGRES_HOST'),
        'NAME': getenv('POSTGRES_DB'),
        'PORT': getenv('POSTGRES_PORT'),
        'USER': getenv('POSTGRES_USER'),
        'PASSWORD': getenv('POSTGRES_PASSWORD'),

    }
}



# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
 
USE_I18N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / "staticfiles")

AUTH_USER_MODEL = "user_auth.User"
# AUTH_USER_MODEL = "core_apps.user_auth.User"

REST_FRAMEWORK= {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"
}

SPECTACULAR_SETTING = {
    "TITLE": "NextGen Bank API",
    "DESCRIPTION": "An API built for a banking system",
    "VERSION": "1.0.0",
    "SERV_INCLUDE_SCHEMA": False,
    "LICENSE" : {
        "name" : "GPL License",
        "url": "https://opensource.org/license/gpl"
    }
}
LOGGING_CONFIG = None
LOGURU_CONFIG = {
    "handlers": [
        {
            "sink" : BASE_DIR / "logs/debug.log",
            "level": "DEBUG",
            "filter": lambda record: record["level"].no == logger.level("DEBUG").no,
            "format":"{time:YYYY-MM-DD : HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
                     "{message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression" : "zip"
        },
        {
            "sink" : BASE_DIR / "logs/info.log",
            "level": "INFO",
            "filter": lambda record: record["level"].no == logger.level("INFO").no,

            "format":"{time:YYYY-MM-DD : HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
                     "{message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression" : "zip",
            "backtrace": True,
            "diagnose": True
        },
        {
            "sink" : BASE_DIR / "logs/warning.log",
            "level": "WARNING",
            "filter": lambda record: record["level"].no == logger.level("WARNING").no,
            "format":"{time:YYYY-MM-DD : HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
                     "{message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression" : "zip",
            "backtrace": True,
            "diagnose": True
        },
        {
            "sink" : BASE_DIR / "logs/error.log",
            "level": "ERROR",
            "filter": lambda record: record["level"].no == logger.level("ERROR").no,

            "format":"{time:YYYY-MM-DD : HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
                     "{message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression" : "zip",
            "backtrace": True,
            "diagnose": True
        },
        {
            "sink" : BASE_DIR / "logs/critical.log",
            "filter": lambda record: record["level"].no == logger.level("CRITICAL").no,
            "level": "CRITICAL",
             "format":"{time:YYYY-MM-DD : HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
                     "{message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression" : "zip",
            "backtrace": True,
            "diagnose": True
        },

    ],
}
logger.configure(**LOGURU_CONFIG)

LOGGIN= {
    "version":1,
    "disable_existing_loggers": False,
    "handlers": {"loguru": {"class": "interceptor.InterceptHandler"}},
    "root": {'handlers': ["loguru"], "level":"DEBUG"}
}


