 
from pathlib import Path
from loguru import logger

from dotenv import load_dotenv
from os import path, getenv
from datetime import timedelta, date


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "core_apps"

local_env_file = path.join(BASE_DIR, ".envs", ".envs.local")
if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# ================== Application definition ==================

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

# ================== middleware ==================

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

# ================== templates configs ==================

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





# ================== Database ==================
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



# ================== Password validation ==================

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# ================== Internationalization ==================
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
 
USE_I18N = True

USE_TZ = True

SITE_ID = 1

# ================== Static files ================== (
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / "staticfiles")

WSGI_APPLICATION = 'config.wsgi.application'
ROOT_URLCONF = 'config.urls'

# ================== User Configs ==================
AUTH_USER_MODEL = "user_auth.User"
DEFAULT_BIRTH_DATE=date(1900,1,1)
DEFAULT_DATE= date(2000,1,1)
DEFAULT_EXPIRY_DATE = date(2030,1,1)
DEFAULT_COUNTRY= "IR"
DEFAULT_PHONE_NUMBER="+989373061991"


# ================== API Service Config ==================
REST_FRAMEWORK= {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATED_CLASSES": [
       "core_apps.common.cookie_auth.CookieAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
       "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_FILTER_BACKEND": [
        "django_filter.rest_framework.DjangoFilterBackend"
    ],
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTILE_CLASSES":[
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATE":{
        "anon": "50/day",
        "user": "100/day",
    }

}

SIMPLE_JWT={
    "SIGNING_KEY":getenv("SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
    "ROTATE_REFRESH_TOKENS": True,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",

}

DJOSER = {
    "USER_ID_FIELD":"id",
    "LOGIN_FIELD":"email",
    "TOKEN_MODEL":None,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL":True,
    "PASSWORD_CHANGE_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_CONFORM_RETYPE": True,
    "PASSWORD_RESET_CONFORM_URL": "password-reset/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SERIALIZERS": {
        "user_create": "core_apps.user_auth.serializers.UserCreateSerializer"
    }
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

# =================== logging ======================

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



# ================= celery ===================

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_TASK_SEND_SENT_EVENT  = True
CELERY_RESULT_EXTENDED  = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY  = True
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT =  60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_WORKER_SEND_TASK_EVENTS = True


# ================ cookies ====================

COOKIE_NAME = "access"
COOKIE_SAMESITE = "Lax"
COOKIE_PATH = "/"
COOKIE_HTTPONLY = True
COOKIE_SECURE=getenv("COOKIE_SECURE", "True") == "True"

