from pathlib import Path

from django.conf.global_settings import PASSWORD_HASHERS
from dotenv import load_dotenv
from os import getenv, path
from loguru import logger
from datetime import timedelta


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = BASE_DIR / "core_apps"

local_env_file = path.join(BASE_DIR, ".envs", '.env.local')

if path.isfile(local_env_file):
    load_dotenv(dotenv_path=local_env_file)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",

]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "django_filters",
    "phonenumber_field",
    "drf_spectacular",
    "djoser",
    "cloudinary",
    "djcelery_email",
    "django_celery_beat"
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.user_profile",
    "core_apps.user_auth",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = 'user_auth.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'core_apps.user_auth.middleware.CustomHeadersMiddleware',
]
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / 'templates')],
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

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

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

SITE_ID = 1

LOGGING_CONFIG = None

LOGURU_LOGGING = {
    'handlers':[
        {
            "sink": BASE_DIR / "log/debug.log",
            "level": "DEBUG",
            "filter": lambda record: record['level'].no <= logger.level("WARNING").no,
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSSS} | {level:<8} | {name}:{function}:{line} - {message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression": "zip",
        },{
            "sink": BASE_DIR / "log/error.log",
            "level": "ERROR",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSSS} | {level:<8} | {name}:{function}:{line} - {message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression": "zip",
            "backtrace": True,
            "diagnose": True,
        }
    ]
}

logger.configure(**LOGURU_LOGGING)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handles":{"loguru":{"class":"interceptor.InterceptorHandler"}},
    "root": {"level": "INFO", "handlers": ["loguru"]},

}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME":getenv("POSTGRES_DB"),
        "USER":getenv("POSTGRES_USER"),
        "PASSWORD":getenv("POSTGRES_PASSWORD"),
        "HOST":getenv("POSTGRES_HOST"),
        "PORT":getenv("POSTGRES_PORT"),
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': str(getenv("BANK_NAME")) + 'API',
    "DESCRIPTION": 'API BUILD for out bank system',
    'VERSION': '1.0.0.',
    'SERVE_INCLUDE_SCHEMA': False,
    'LICENSE':{
        'name':'MIT License',
    }
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}