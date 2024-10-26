import unittest
from unittest.mock import AsyncMock, Mock

from models.product import Product
from repository.product_repository_manager import ProductRepositoryManager
from repository.cache.base_cache import ICache
from repository.storage.base_storage import IStorage
from services.image_downloader import ImageDownloader

class TestProductRepositoryManager(unittest.TestCase):

    def setUp(self):
        self.cache = Mock(spec=ICache)
        self.storage = Mock(spec=IStorage)
        self.image_downloader = Mock(spec=ImageDownloader)
        self.manager = ProductRepositoryManager(self.cache, self.storage, self.image_downloader)

    @AsyncMock
    async def test_sync_products_success(self):
        products = [
            Product(product_title="Product 1", product_price=100.0, path_to_image_public="https://dentalstall.com/wp-content/uploads/2021/06/transbond-mip-primer-bottle_02-300x300.jpg"),
            Product(product_title="Product 2", product_price=200.0, path_to_image_public="https://dentalstall.com/wp-content/uploads/2022/01/d-pulp-300x300.jpg"),
        ]

        self.cache.get.side_effect = [None, None]
        self.image_downloader.download_image.side_effect = ["local_path_image1", "local_path_image2"]
        self.cache.add.side_effect = [None, None]
        self.storage.add.side_effect = [None, None]

        await self.manager.sync_products(products)

        self.assertEqual(self.cache.add.call_count, 2)
        self.assertEqual(self.storage.add.call_count, 2)

    @AsyncMock
    async def test_sync_single_product_update_image(self):
        product = Product(product_title="Product 1", product_price=100.0, path_to_image_public="https://dentalstall.com/wp-content/uploads/2021/06/transbond-mip-primer-bottle_02-300x300.jpg")
        cached_product = {'product_price': 100.0, 'path_to_image_public': "https://dentalstall.com/wp-content/uploads/2022/01/cavitonava9-300x300.jpg"}

        self.cache.get.return_value = cached_product
        self.image_downloader.download_image.return_value = "local_path_image_updated"
        self.cache.update.return_value = None
        self.storage.update.return_value = None

        await self.manager.sync_single_product(product)

        self.image_downloader.download_image.assert_called_once_with("https://dentalstall.com/wp-content/uploads/2021/06/transbond-mip-primer-bottle_02-300x300.jpg")
        self.cache.update.assert_called_once()
        self.storage.update.assert_called_once()

    @AsyncMock
    async def test_sync_single_product_update_price(self):
        product = Product(product_title="Product 1", product_price=150.0, path_to_image_public="https://dentalstall.com/wp-content/uploads/2021/06/transbond-mip-primer-bottle_02-300x300.jpg")
        cached_product = {'product_price': 100.0, 'path_to_image_public': "https://dentalstall.com/wp-content/uploads/2021/06/transbond-mip-primer-bottle_02-300x300.jpg"}

        self.cache.get.return_value = cached_product
        self.image_downloader.download_image.return_value = "local_path_image"
        self.cache.update.return_value = None
        self.storage.update.return_value = None

        await self.manager.sync_single_product(product)

        self.assertEqual(cached_product['product_price'], 150.0)
        self.cache.update.assert_called_once()
        self.storage.update.assert_called_once()

    @AsyncMock
    async def test_sync_single_product_new_product(self):
        product = Product(product_title="Product 1", product_price=100.0, path_to_image_public="https://dentalstall.com/wp-content/uploads/2021/06/transbond-mip-primer-bottle_02-300x300.jpg")
        
        self.cache.get.return_value = None
        self.image_downloader.download_image.return_value = "local_path_image"
        self.cache.add.return_value = None
        self.storage.add.return_value = None

        await self.manager.sync_single_product(product)

        self.cache.add.assert_called_once()
        self.storage.add.assert_called_once()

if __name__ == '__main__':
    unittest.main()
