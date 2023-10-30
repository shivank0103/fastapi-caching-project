import time
import requests
from caching.local_cache import LocMemCache
from caching import CashifyCache
from caching.redis_cache import RedisCache


REDIS_URL = 'redis://172.16.1.29:6379/10'

redis_cache = RedisCache(REDIS_URL)
local_cache = LocMemCache()

cache = CashifyCache('tt', 'LOCAL')


@cache.cache(namespace='test1', timeout=60, keys=[])
def t1(var1, var2):
    print(time.time())
    # if local_cache.get('tt', None):
    #     print(time.time())
    #     return local_cache.get('tt')
    response = requests.get('https://caddy.community/t/using-zerossls-acme-endpoint/9406')

    # local_cache.set('tt', response, 60)
    print(time.time())
    print(response)
    # print(redis_cache.get('tttest1'), 'c_result')
    # print(time.time())
    return response


if __name__ == '__main__':
    print(t1('2',var2='1'))
