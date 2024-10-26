import asyncio
import logging
from typing import List

from .cache.base_cache import ICache
from .storage.base_storage import IStorage
from models.product import Product
from services.image_downloader import ImageDownloader
from repository.product_repository import IProductRepository

logger = logging.getLogger(__name__)

class ProductRepositoryManager(IProductRepository):
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
                product_updated = False
                if cached_product['path_to_image_public'] != product.path_to_image_public:
                    image_path = await self.image_downloader.download_image(product.path_to_image_public)
                    product.path_to_image = image_path
                    product_updated = True
                
                if cached_product['product_price'] != product.product_price:
                    cached_product['product_price'] = product.product_price
                    product_updated = True

                if product_updated:
                    await asyncio.gather(
                        self.cache.update(redis_key, product),
                        self.storage.update(product)
                    )
            else:
                image_path = await self.image_downloader.download_image(product.path_to_image_public)
                product.path_to_image = image_path

                await asyncio.gather(
                    self.cache.add(redis_key, product),
                    self.storage.add(product)
                )

        except Exception as e:
            logger.error(f"Error syncing product {product.product_title}: {e}")
            raise e