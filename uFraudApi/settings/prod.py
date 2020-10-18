from .base import *

'''
this file is for internal usage only, whenever i may have to make migrations, i can connect to it via the local app
and be done with it
'''

CELERY_BROKER_URL = 'redis://h:pc6c586d35c82a4c6dbfd1ca940bbec02ded3af2098fe0019e8d2145b8ee40624@ec2-50-16-240-35.compute-1.amazonaws.com:18709'
#
# DATABASES = {
#
#     'default': {
#
#         'ENGINE': 'django.db.backends.postgresql',
#
#         'NAME': 'd5k6r7neqjv7cl',
#
#         'USER': 'jcwhtrhlznqqri',
#
#         'PASSWORD': '61c8859c27c769819ec7b91d2f932b248d12bfd047e2e932b8be55e79a3360aa',
#
#         'HOST': 'ec2-3-222-150-253.compute-1.amazonaws.com',
#
#         'PORT': '5432',
#
#     }
#
# }

DATABASES = {

        'default': {

            'ENGINE': 'django.db.backends.postgresql',

            'NAME': 'd9c0nluu7dv5e8',

            'USER': 'ieidkekrasxwji',

            'PASSWORD': '4384cf08085469fe6501bf57bb4ea10a16d048a01fd07039dde636375aa6cc64',

            'HOST': 'ec2-54-164-134-207.compute-1.amazonaws.com',

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
