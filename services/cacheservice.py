from django.core.cache import cache


def rate_limit(key, timeout=5):
    if key not in cache:
        cache.set(key, 0, timeout=60*timeout)
    cache.incr(key, delta=1)
    return cache.get(key)
