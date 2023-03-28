import os
from pathlib import Path

from dotenv import load_dotenv

from .base import *

# Dotenv config:

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Prod config

DEBUG = False

ALLOWED_HOSTS = ["tutor-production-d86c.up.railway.app",
                "127.0.0.1",
                ]

SECRET_KEY = os.environ.get("PROD_SECRET_KEY")

CSRF_TRUSTED_ORIGINS = ["https://tutor-production-d86c.up.railway.app"]

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": os.environ.get("PROD_DB_NAME"),
        "USER": os.environ.get("PROD_DB_USER"),
        "PASSWORD": os.environ.get("PROD_DB_PS"),
        "HOST": os.environ.get("PROD_DB_HOST"),
        'PORT': '6847',
    }
}

# AWS S3

AWS_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_HOST = "s3.eu-central-1.amazonaws.com"
AWS_S3_REGION_NAME = "eu-central-1"

AWS_QUERYSTRING_AUTH = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True