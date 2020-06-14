web: gunicorn uFraudApi.wsgi --log-file -
worker: celery -A uFraudApi worker -B --loglevel=info

