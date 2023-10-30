import inspect, itertools
from enum import Enum
from caching.local_cache import LocMemCache
from caching.redis_cache import RedisCache


class CacheType(Enum):
    LOCAL_CACHE = 'LOCAL'
    REDIS_CACHE = 'REDIS'


class CashifyCache:
    app_name: str = None
    cache_type: str = None
    redis_cache_url: str = None

    local_cache = None
    redis_cache = None

    def __init__(self, app_name: str, cache_type: str, redis_cache_url: str = None) -> None:
        self.app_name = app_name
        if cache_type not in [item.value for item in CacheType]:
            raise Exception("Please provide correct cache type, either 'LOCAL' or 'REDIS'")
        self.cache_type = cache_type
        if self.cache_type == CacheType.REDIS_CACHE.value and redis_cache_url is None:
            raise Exception("In case of remote cache please provide remote cache URL")
        elif self.cache_type == CacheType.LOCAL_CACHE.value:
            self.local_cache = LocMemCache()
        elif self.cache_type == CacheType.REDIS_CACHE.value:
            self.redis_cache = RedisCache(redis_cache_url)

    def cache(self, namespace: str, timeout: int, keys: list[str]):
        def cache_func(func):
            def wrapper(*args, **kwargs):

                suffix = ''
                args_name = inspect.getfullargspec(func)[0]
                args_dict = dict(zip(args_name, args))

                all_keys = [*args_dict] + [*kwargs]
                if not set(keys).issubset(all_keys):
                    raise Exception("Please provide correct keys")

                all_args = args_dict | kwargs
                for key in keys:
                    suffix += '.' + key + '.' + all_args.get(key)
                required_key = self.app_name + '.' + namespace + '.' + func.__name__ + suffix
                if self.cache_type == CacheType.LOCAL_CACHE.value:
                    cache_response = self.local_cache.get(required_key)
                else:
                    cache_response = self.redis_cache.get(required_key)
                if cache_response is not None:
                    return cache_response

                response = func(*args, **kwargs)
                if self.cache_type == CacheType.LOCAL_CACHE.value:
                    self.local_cache.set(required_key, response, timeout)
                else:
                    self.redis_cache.set(required_key, response, timeout)
                return response

            return wrapper

        return cache_func
