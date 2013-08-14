from django.conf import settings
from django.core.cache import cache
import cPickle as pickle
import hashlib


def cache_function(length):
    """
    A variant of the snippet posted by Jeff Wheeler at
    http://www.djangosnippets.org/snippets/109/

    Caches a function, using the function and its arguments as the key, and the return
    value as the value saved. It passes all arguments on to the function, as
    it should.

    The decorator itself takes a length argument, which is the number of
    seconds the cache will keep the result around.
    """
    def decorator(func):
        def inner_func(*args, **kwargs):
            if hasattr(settings, 'IS_IN_UNITTEST'):
                return func(*args, **kwargs)

            raw = [func.__name__, func.__module__, args, kwargs]
            pickled = pickle.dumps(raw, protocol=pickle.HIGHEST_PROTOCOL)
            key = hashlib.md5(pickled).hexdigest()
            value = cache.get(key)

            if key in cache:
                return value
            else:
                result = func(*args, **kwargs)
                cache.set(key, result, length)
                return result
        return inner_func
    return decorator
