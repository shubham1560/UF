from django.core.cache import cache
from decouple import config


def rate_limit(key, timeout=5):
    if key not in cache:
        cache.set(key, 0, timeout=60*timeout)
    cache.incr(key, delta=1)
    return cache.get(key)


def clear_all():
    cache.clear()


def cache_enable():
    # print("enable cache running")
    return True