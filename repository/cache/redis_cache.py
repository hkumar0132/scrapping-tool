import json
import redis.asyncio as redis
import logging
from typing import Optional

from models.product import Product
from .base_cache import ICache

logger = logging.getLogger(__name__)

class RedisCache(ICache):
    _instance = None

    def __new__(cls, redis_url: str):
        if cls._instance is None:
            cls._instance = super(RedisCache, cls).__new__(cls)
            try:
                cls._instance.client = redis.from_url(redis_url, decode_responses=True)
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        return cls._instance

    async def get(self, key: str) -> Optional[dict]:
        try:
            cached_product = await self.client.get(key)
            if cached_product:
                return json.loads(cached_product)
            else:
                return None
        except Exception as e:
            logger.error(f"Error while getting cache for key {key}: {e}")
            return None

    async def add(self, key: str, product: Product) -> None:
        try:
            await self.client.set(key, product.json())
        except Exception as e:
            logger.error(f"Error while adding product to cache with key {key}: {e}")
            raise

    async def update(self, key: str, product: Product) -> None:
        try:
            await self.client.set(key, product.json())
        except Exception as e:
            logger.error(f"Error while updating product in cache with key {key}: {e}")
            raise

    async def delete(self, key: str) -> None:
        try:
            await self.client.delete(key)
        except Exception as e:
            logger.error(f"Error while deleting product from cache with key {key}: {e}")
            raise
