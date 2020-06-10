from .base import *

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': config('DB_NAME_DEV'),

        'USER': 'jcwhtrhlznqqri',

        'PASSWORD': '61c8859c27c769819ec7b91d2f932b248d12bfd047e2e932b8be55e79a3360aa',

        'HOST': 'ec2-3-222-150-253.compute-1.amazonaws.com',

        'PORT': '5432',

    }

}