import os

from dotenv import load_dotenv

from .base import *

# Dotenv config:

env_path = '.env'
load_dotenv(dotenv_path=env_path)

# Prod config

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "railway.app"]

SECRET_KEY = os.environ.get("PROD_SECRET_KEY")

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": os.environ.get("PROD_DB_NAME"),
        "USER": os.environ.get("PROD_DB_USER"),
        "PASSWORD": os.environ.get("PROD_DB_PS"),
        "HOST": os.environ.get("PROD_DB_HOST"),
        'PORT': '6073',
    }
}