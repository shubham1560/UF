from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
# CELERY_BROKER_URL = 'redis://h:pc420dcd443a7edd61e683c8ef3e335d5f146d4ea54218667ab9297ae11ed0dca@ec2-52-23-127-211.' \
#                      'compute-1.amazonaws.com:7419'

CELERY_BROKER_URL = "redis://rediscloud:pJUD3PHSRsTf0AK6luOVUTciPS8XMwgI@redis-17645.c14.us-east-1-2.ec2.cloud." \
                        "redislabs.com:17645"


DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'postgres',

        'USER': 'postgres',

        'PASSWORD': 'Olabola@12',

        'HOST': '127.0.0.1',

        'PORT': '5432',

    }

}

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


#
# DATABASES = {
#
#     'default': {
#
#         'ENGINE': 'django.db.backends.postgresql',
#
#         'NAME': 'defaultdb',
#
#         'USER': 'doadmin',
#
#         'PASSWORD': 'mu4dfunuqhu1fy23',
#
#         'HOST': 'db-postgresql-blr1-63156-do-user-7592334-0.b.db.ondigitalocean.com',
#
#         'PORT': '25060',
#
#     }
#
# }


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % ("ec2-52-23-127-211.compute-1.amazonaws.com", "7419"),
        'OPTIONS': {
            'PASSWORD': "pc420dcd443a7edd61e683c8ef3e335d5f146d4ea54218667ab9297ae11ed0dca",
            'DB': 0,
        }
    }
}

CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '%s:%s' % ("redis-17645.c14.us-east-1-2.ec2.cloud.redislabs.com", "17645"),
            'OPTIONS': {
                'PASSWORD': "pJUD3PHSRsTf0AK6luOVUTciPS8XMwgI",
                'DB': 0,
            }
        }
    }

#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }


AWS_STORAGE_BUCKET_NAME = 'sortedtree-test'

CELERY_RESULT_BACKEND = 'db+postgresql://postgres:Olabola@12@localhost/uf-db-django'