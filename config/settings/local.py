from os import getenv, path
from dotenv import load_dotenv

from .base import * # noqa
from .base import BASE_DIR


local_env_file = path.join(BASE_DIR, ".envs", '.env.local')
if path.isfile(local_env_file):
    load_dotenv(dotenv_path=local_env_file)


# SECURITY WARNING: keep the secret key used in production.txt secret!
SECRET_KEY = getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production.txt!
DEBUG = getenv('DEBUG')

ALLOWED_HOSTS = ['0.0.0.0']

SITE_NAME = getenv('SITE_NAME')
ADMIN_URL = getenv('ADMIN_URL')


EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = getenv('EMAIL_PORT')
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL')
DOMAIN = getenv('DOMAIN')

MAX_UPLOAD_SIZE = 1 * 1024 * 1024

CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']

ALLOWED_HOSTS = ['localhost']

LOCKOUT_DURATION = timedelta(minutes=1)

LOGIN_ATTEMPTS = 3
OTP_EXPIRATION = timedelta(minutes=1)
