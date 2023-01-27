import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["test-application-prod.herokuapp.com"]

DATABASES = {
    'default': dj_database_url.config()
}

CELERY_BROKER_URL = os.environ.get("REDISCLOUD_URL")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDISCLOUD_URL"),
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = os.environ.get("MAILGUN_SMTP_SERVER")
EMAIL_HOST_USER = os.environ.get("MAILGUN_SMTP_LOGIN")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_SMTP_PASSWORD")
EMAIL_PORT = os.environ.get("MAILGUN_SMTP_PORT")