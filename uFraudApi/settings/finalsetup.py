from .base import *

ALLOWED_HOSTS = ['database1560.herokuapp.com', 'uf-api.herokuapp.com', 'uf-preprod.herokuapp.com']

AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')


if config('PRODUCTION') == '0':

    # Non Production
    CELERY_BROKER_URL = "redis://rediscloud:pJUD3PHSRsTf0AK6luOVUTciPS8XMwgI@redis-17645.c14.us-east-1-2.ec2.cloud." \
                        "redislabs.com:17645"

    DEBUG = config('DEBUG') == 'True'

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

    DATABASES = {

        'default': {

            'ENGINE': 'django.db.backends.postgresql',

            'NAME': 'd1r2iam6t73l4b',

            'USER': 'uaofyovxrlstew',

            'PASSWORD': '207fe27a60a73ea6506282e4e165932738c4e3ff151eb5587a6980a1f7490723',

            'HOST': 'ec2-54-86-170-8.compute-1.amazonaws.com',

            'PORT': '5432',

        }

    }

else:

    # Production

    DEBUG = config('DEBUG') == 'True'

    # CELERY_BROKER_URL = "redis://h:pc6c586d35c82a4c6dbfd1ca940bbec02ded3af2098fe0019e8d2145b8ee40624@ec2-50-16-240-35."\
    #                     "compute-1.amazonaws.com:18709"

    CELERY_BROKER_URL = "redis://rediscloud:ok3AlmhlYZMSk7bQsfFhqri5c3d5dBJJ@redis-14029.c73.us-east-1-2.ec2." \
                        "cloud.redislabs.com:14029"
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

    # CACHES = {
    #     'default': {
    #         'BACKEND': 'redis_cache.RedisCache',
    #         'LOCATION': '%s:%s' % ("ec2-50-16-240-35.compute-1.amazonaws.com", "18709"),
    #         'OPTIONS': {
    #             'PASSWORD': "pc6c586d35c82a4c6dbfd1ca940bbec02ded3af2098fe0019e8d2145b8ee40624",
    #             'DB': 0,
    #         }
    #     }
    # }

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '%s:%s' % ("redis-14029.c73.us-east-1-2.ec2.cloud.redislabs.com", "14029"),
            'OPTIONS': {
                'PASSWORD': "ok3AlmhlYZMSk7bQsfFhqri5c3d5dBJJ",
                'DB': 0,
            }
        }
    }
