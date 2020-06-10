from .base import *

ALLOWED_HOSTS = ['database1560.herokuapp.com', 'uf-api.herokuapp.com']


if config('PRODUCTION') == '0':

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
            'LOCATION': '%s:%s' % ("ec2-50-16-240-35.compute-1.amazonaws.com", "18709"),
            'OPTIONS': {
                'PASSWORD': "pc6c586d35c82a4c6dbfd1ca940bbec02ded3af2098fe0019e8d2145b8ee40624",
                'DB': 0,
            }
        }
    }



