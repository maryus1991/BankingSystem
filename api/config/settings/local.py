from django.conf.global_settings import CSRF_TRUSTED_ORIGINS
from dotenv import load_dotenv
from os import path, getenv

from .base import * # noqa
from .base import BASE_DIR



local_env_file = path.join(BASE_DIR , ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


SECRET_KEY = getenv("SECRET_KEY") # 'django-insecure-4i^oj-*s34y8*$5@*s1p7b=k9ukn6n-t0&*6=-^o$^1ghvf$vh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG") 

SITE_NAMAE = getenv("SITE_NAME") 

ALLOWED_HOSTS = ["localhost", "0.0.0.0"]

ADMIN_URL = getenv("ADMIN_URL")

EMAIL_BACKEND = "djceley_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

MAX_UPLOAD_SIZE = 1 * 1024 * 1024

CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']


LOCKOUT_DURATION = timedelta(minutes=1)
LOGIN_ATTEMPTS= 3
OTP_EXPIRATION= timedelta(minutes=1)
SECURE_SSL_REDIRECT = False


MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / "media")
