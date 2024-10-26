from .redis_cache import RedisCache
from .base_cache import ICache
from .enums import CacheType
from config import Config

class CacheFactory:
    @staticmethod
    def get_cache(cache_type: CacheType) -> ICache:
        if cache_type == CacheType.REDIS:
            return RedisCache(Config.REDIS_URL)
        raise ValueError("Invalid cache type")
