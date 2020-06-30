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

AWS_STORAGE_BUCKET_NAME = 'urbanfraud-test'

CELERY_RESULT_BACKEND = 'db+postgresql://postgres:Olabola@12@localhost/uf-db-django'