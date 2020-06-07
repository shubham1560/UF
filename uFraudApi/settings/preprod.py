from .base import *

ALLOWED_HOSTS = ['database1560.herokuapp.com']

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