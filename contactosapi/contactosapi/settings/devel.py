from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "contactosapi",
        "USER": "root",
        "PASSWORD": "rage",
        "HOST": "172.17.0.2",
        "PORT": "",
    }
    
}

INSTALLED_APPS += ("debug_toolbar", 'django_extensions',)
INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE += \
    ("debug_toolbar.middleware.DebugToolbarMiddleware", )

CORS_ORIGIN_WHITELIST = [
    "http://localhost:4200", # "https://rbarrero.duckdns.org:442",
]