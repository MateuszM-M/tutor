from .base import *

# Dev config

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

SECRET_KEY = 'django-insecure-6%)%txlwh)+rqmv8s)frvz!tx3wh)%!2h=9rl&thp66)i0gk=i'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# DJANGO DEBUG TOOLBAR SETTINGS FOR DOCKER

if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]