from functools import partial

from django.core.cache import cache, InvalidCacheBackendError
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.utils.decorators import method_decorator
from django.views.generic import View

from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.core import (get_usage, is_ratelimited,
                                   _split_rate, _get_ip)


rf = RequestFactory()


class MockUser:
    def __init__(self, authenticated=False):
        self.pk = 1
        self.is_authenticated = authenticated


class RateParsingTests(TestCase):
    def test_simple(self):
        pass


def callable_rate(group, request):
    pass


def mykey(group, request):
    pass


class CustomRatelimitedException(Exception):
    pass


class RatelimitTests(TestCase):
    def setUp(self):
        pass

    def test_no_key(self):
        @ratelimit(rate='1/m')
        pass

    def test_ip(self):
        @ratelimit(key='ip', rate='1/m', block=False)
        pass

    def test_block(self):
        @ratelimit(key='ip', rate='1/m')
        pass

    def test_ratelimit_custom_string_exception_class(self):
        @ratelimit(key='ip', rate='1/m')
        pass

    def test_ratelimit_custom_exception_class(self):
        @ratelimit(key='ip', rate='1/m')
        pass

    def test_method(self):
        @ratelimit(key='ip', method='POST', rate='1/m', group='a', block=False)
        pass

    def test_unsafe_methods(self):
        @ratelimit(key='ip', method=ratelimit.UNSAFE, rate='0/m', block=False)
        pass

    def test_key_get(self):
        @ratelimit(key='get:foo', rate='1/m', method='GET', block=False)
        pass

    def test_key_post(self):
        @ratelimit(key='post:foo', rate='1/m', block=False)
        pass

    def test_key_header(self):
        pass

    def test_rate(self):
        @ratelimit(key='ip', rate='2/m', block=False)
        pass

    def test_zero_rate(self):
        @ratelimit(key='ip', rate='0/m', block=False)
        pass

    def test_none_rate(self):
        @ratelimit(key='ip', rate=None, block=False)
        pass

    def test_callable_rate(self):
        pass

    def test_callable_rate_none(self):
        pass

    def test_callable_rate_zero(self):
        pass

    def test_callable_rate_import(self):
        pass

    def test_user_or_ip(self):
        """Allow custom functions to set cache keys."""
        pass

    def test_callable_key_path(self):
        @ratelimit(key='django_ratelimit.tests.mykey', rate='1/m', block=False)
        pass

    def test_callable_key(self):
        @ratelimit(key=mykey, rate='1/m', block=False)
        pass

    def test_stacked_decorator(self):
        """Allow @ratelimit to be stacked."""
        pass

    def test_stacked_methods(self):
        """Different methods should result in different counts."""
        pass

    def test_sorted_methods(self):
        """Order of the methods shouldn't matter."""
        pass

    def test_ratelimit_full_mask_v4(self):
        @ratelimit(rate='1/m', key='ip', block=False)
        pass

    def test_ratelimit_full_mask_v6(self):
        @ratelimit(rate='1/m', key='ip', block=False)
        pass

    def test_ratelimit_mask_v4(self):
        @ratelimit(rate='1/m', key='ip', block=False)
        pass

    def test_ratelimit_mask_v6(self):
        @ratelimit(rate='1/m', key='ip', block=False)
        pass


class FunctionsTests(TestCase):
    def setUp(self):
        pass

    def test_is_ratelimited(self):
        pass

    def test_is_ratelimited_increment(self):
        pass

    def test_get_usage(self):
        pass

    def test_get_usage_increment(self):
        pass

    def test_not_increment_after_increment(self):
        pass

    def test_get_usage_called_without_group_or_fn(self):
        pass


class RatelimitCBVTests(TestCase):
    def setUp(self):
        pass

    def test_method_decorator(self):
        pass

    def test_class_decorator(self):
        @method_decorator(ratelimit(key='ip', rate='1/m', block=False),
                          name='get')
        pass

    def test_wrap_view(self):
        pass

    def test_methods_counted_separately(self):
        pass

    def test_views_counted_separately(self):
        pass


class CacheFailTests(TestCase):
    @override_settings(RATELIMIT_USE_CACHE='fake-cache')
    def test_bad_cache(self):
        @ratelimit(key='ip', rate='1/m', block=False)
        pass

    @override_settings(RATELIMIT_USE_CACHE='connection-errors')
    def test_limit_on_cache_connection_error(self):
        @ratelimit(key='ip', rate='10/m', block=False)
        pass

    @override_settings(RATELIMIT_USE_CACHE='connection-errors',
                       RATELIMIT_FAIL_OPEN=True)
    def test_fail_open_setting(self):
        @ratelimit(key='ip', rate='1/m', block=False)
        pass

    @override_settings(RATELIMIT_USE_CACHE='connection-errors')
    def test_is_ratelimited_cache_connection_error_without_increment(self):
        pass

    @override_settings(RATELIMIT_USE_CACHE='connection-errors')
    def test_is_ratelimited_cache_connection_error_with_increment(self):
        pass

    @override_settings(RATELIMIT_USE_CACHE='connection-errors-redis')
    def test_is_ratelimited_cache_connection_error_with_increment_redis(self):
        pass

    @override_settings(RATELIMIT_USE_CACHE='instant-expiration')
    def test_cache_timeout(self):
        @ratelimit(key='ip', rate='1/m')
        pass


def my_ip(req):
    pass


class IpMetaTests(TestCase):
    def test_default(self):
        pass

    @override_settings(RATELIMIT_IP_META_KEY='fake')
    def test_bad_config(self):
        pass

    @override_settings(RATELIMIT_IP_META_KEY='HTTP_X_CLIENT_IP')
    def test_alternate_header(self):
        pass

    @override_settings(RATELIMIT_IP_META_KEY='django_ratelimit.tests.my_ip')
    def test_path_to_ip_key_callable(self):
        pass

    @override_settings(RATELIMIT_IP_META_KEY=my_ip)
    def test_callable_ip_key(self):
        pass

    def test_empty_ip(self):
        pass
