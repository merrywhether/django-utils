from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import iri_to_uri, smart_str
from django.utils.translation import get_language
import hashlib


def make_key(key, key_prefix, version):
    # This is the default django cache key generator. Only useful for debugging what the cache key will be.
    cache_key = ':'.join([key_prefix, str(version), smart_str(key)])
    # print 'make_key', cache_key
    return cache_key


def delete_url_cache(url):
    cache_key = url_cache_key(url)
    # print 'Deleting cache_key', cache_key
    cache.delete(cache_key)


def url_cache_key(url, language=None, key_prefix=None):
    if key_prefix is None:
        # The cache_page decorator doesn't use the key prefix to generate it's key, so we shouldn't either.
        # key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
        key_prefix = ''

    ctx = hashlib.md5()
    path = hashlib.md5(iri_to_uri(url))

    cache_key = 'views.decorators.cache.cache_page.%s.%s.%s.%s' % (
        key_prefix, 'GET', path.hexdigest(), ctx.hexdigest())

    if settings.USE_I18N:
        cache_key += '.%s' % (language or get_language())

    return cache_key
