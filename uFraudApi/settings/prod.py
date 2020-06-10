from .base import *

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'd5k6r7neqjv7cl',

        'USER': 'jcwhtrhlznqqri',

        'PASSWORD': '61c8859c27c769819ec7b91d2f932b248d12bfd047e2e932b8be55e79a3360aa',

        'HOST': 'ec2-3-222-150-253.compute-1.amazonaws.com',

        'PORT': '5432',

    }

}

CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '%s:%s' % ("ec2-50-16-240-35.compute-1.amazonaws.com", "7419"),
            'OPTIONS': {
                'PASSWORD': "pc420dcd443a7edd61e683c8ef3e335d5f146d4ea54218667ab9297ae11ed0dca",
                'DB': 0,
            }
        }
    }
