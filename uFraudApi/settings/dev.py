from .base import *

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': config('DB_NAME_DEV'),

        'USER': 'postgres',

        'PASSWORD': 'Olabola@12',

        'HOST': '127.0.0.1',

        'PORT': '5432',

    }

}