from __future__ import absolute_import, unicode_literals
from .settings import dev
from .settings import base
import os

from celery import Celery
from decouple import config
# set the default Django settings module for the 'celery' program.


if config('LIVE') == '0':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uFraudApi.settings.dev')
    app = Celery('uFraudApi',
                 broker="redis://rediscloud:pJUD3PHSRsTf0AK6luOVUTciPS8XMwgI@redis-17645.c14.us-east-1-2.ec2.cloud."
                        "redislabs.com:17645")

else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uFraudApi.settings.finalsetup')
    app = Celery('uFraudApi',
                 broker="redis://rediscloud:pJUD3PHSRsTf0AK6luOVUTciPS8XMwgI@redis-17645.c14.us-east-1-2.ec2.cloud."
                        "redislabs.com:17645")


# app = Celery('uFraudApi', broker="redis://h:pc420dcd443a7edd61e683c8ef3e335d5f146d4ea54218667ab9297ae11ed0dca@ec2-52-23-127-211.compute-1.amazonaws.com:7419")

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.autodiscover_tasks(lambda: dev.INSTALLED_APPS)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))