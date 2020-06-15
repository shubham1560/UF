from __future__ import absolute_import, unicode_literals
from .settings import dev
from .settings import finalsetup
import os

from celery import Celery
from decouple import config
# set the default Django settings module for the 'celery' program.


if config('LIVE') == '0':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uFraudApi.settings.dev')
    app = Celery('uFraudApi')
    app.autodiscover_tasks(lambda: dev.INSTALLED_APPS)
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uFraudApi.settings.finalsetup')
    app = Celery('uFraudApi')
    app.autodiscover_tasks(lambda: finalsetup.INSTALLED_APPS)

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