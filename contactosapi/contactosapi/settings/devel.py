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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 15
}
