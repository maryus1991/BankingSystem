from .base import * # noqa

prod_env_file = path.join(BASE_DIR,".envs", ".env.production")

if path.isfile(prod_env_file):
    load_dotenv(prod_env_file)

SECRET_KEY = getenv("SECRET_KEY")
DEBUG = getenv("DEBUG")
SITE_NAME = getenv("SITE_NAME")

ADMINS=[("maryus", "maryus19915123@gmail.com")]

ALLOWS_HOSTS = []
ADMIN_URL = getenv("ADMIN_URL")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")
EMAIL_USE_TLS = True
ADMIN_EMAIL=getenv("ADMIN_EMAIL")

MAX_UPLOAD_SIZE = 1 * 1024 * 1024

CSRF_TRUSTED_ORIGINS = ['']
LOCKOUT_DURATION = timedelta(minutes=1)
LOGIN_ATTEMPTS= 3
OTP_EXPIRATION= timedelta(minutes=1)
SECURE_SSL_REDIRECT = getenv("SECURE_SSL_REDIRECT")
SECURE_PROXY_SSL_HEADER = ()
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS=getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_HSTS_PRELOAD=getenv("SECURE_HSTS_PRELOAD")
SECURE_CONTENT_TYPE_NOSNIFF=getenv("SECURE_CONTENT_TYPE_NOSNIFF")