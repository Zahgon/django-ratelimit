from django.conf import settings
from django.core import checks

SUPPORTED_CACHE_BACKENDS = [
    'django.core.cache.backends.memcached.PyMemcacheCache',
    'django.core.cache.backends.memcached.PyLibMCCache',
    'django_redis.cache.RedisCache',
]

CACHE_FAKE = 'is not a real cache'
CACHE_NOT_SHARED = 'is not a shared cache'
CACHE_NOT_ATOMIC = 'does not support atomic increment'

KNOWN_BROKEN_CACHE_BACKENDS = {
    'django.core.cache.backends.dummy.DummyCache': CACHE_FAKE,
    'django.core.cache.backends.locmem.LocMemCache': CACHE_NOT_SHARED,
    'django.core.cache.backends.filebased.FileBasedCache': CACHE_NOT_ATOMIC,
    'django.core.cache.backends.db.DatabaseCache': CACHE_NOT_ATOMIC,
}


@checks.register(checks.Tags.caches, 'django_ratelimit')
def check_caches(app_configs, **kwargs):
    pass
