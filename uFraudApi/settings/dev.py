from .base import *

DEBUG = True

CELERY_BROKER_URL = 'redis://h:pc420dcd443a7edd61e683c8ef3e335d5f146d4ea54218667ab9297ae11ed0dca@ec2-52-23-127-211.compute-1.amazonaws.com:7419'

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'uf-db-django',

        'USER': 'postgres',

        'PASSWORD': 'Olabola@12',

        'HOST': '127.0.0.1',

        'PORT': '5432',

    }

}


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST_USER = 'avij1560@gmail.com'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_PASSWORD = 'olabola12'

AWS_STORAGE_BUCKET_NAME = 'urbanfraud-test'

CELERY_RESULT_BACKEND = 'db+postgresql://postgres:Olabola@12@localhost/uf-db-django'