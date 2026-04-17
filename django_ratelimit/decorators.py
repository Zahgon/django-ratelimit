from functools import wraps

from django.conf import settings
from django.utils.module_loading import import_string

from django_ratelimit import ALL, UNSAFE
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.core import is_ratelimited


__all__ = ['ratelimit']


def ratelimit(group=None, key=None, rate=None, method=ALL, block=True):
    def decorator(fn):
        @wraps(fn)
        pass
    return decorator


ratelimit.ALL = ALL
ratelimit.UNSAFE = UNSAFE
