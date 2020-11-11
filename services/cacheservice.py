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


def del_key(key):
    cache.delete(key)


def delete_many(array_key):
    cache.delete_many(array_key)


def set_key(key, value):
    cache.set(key, value)


def get_key(key):
    return cache.get(key)


def has_key(key):
    if key in cache:
        return True
    return False