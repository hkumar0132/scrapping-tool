import asyncio
import os
from cache.base_cache import ICache
from storage.base_storage import IStorage
from models.product import Product
from typing import List
import logging
from services.image_downloader import ImageDownloader

logger = logging.getLogger(__name__)

class ProductManager:
    def __init__(self, cache: ICache, storage: IStorage, image_downloader: ImageDownloader):
        self.cache = cache
        self.storage = storage
        self.image_downloader = image_downloader

    async def sync_products(self, products: List[Product]) -> List[Product]:
        tasks = []
        for product in products:
            tasks.append(self.sync_single_product(product))

        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error syncing products: {e}")
            raise e

    async def sync_single_product(self, product: Product) -> None:
        redis_key = f"product:{product.product_title}"

        try:
            cached_product = await self.cache.get(redis_key)
            if cached_product:
                if (cached_product['product_price'] != product.product_price or
                        cached_product['path_to_image'] != product.path_to_image):
                    image_path = await self.image_downloader.download_image(product.path_to_image)
                    product.path_to_image = image_path

                    await asyncio.gather(
                        self.cache.update(redis_key, product),
                        self.storage.update(product)
                    )
            else:
                image_path = await self.image_downloader.download_image(product.path_to_image)
                product.path_to_image = image_path

                await asyncio.gather(
                    self.cache.add(redis_key, product),
                    self.storage.add(product)
                )

        except Exception as e:
            logger.error(f"Error syncing product {product.product_title}: {e}")
            raise e