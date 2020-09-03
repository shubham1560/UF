"""
WSGI config for uFraudApi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from decouple import config

from django.core.wsgi import get_wsgi_application

if config('LIVE') == '0':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uFraudApi.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uFraudApi.settings.finalsetup')

application = get_wsgi_application()





