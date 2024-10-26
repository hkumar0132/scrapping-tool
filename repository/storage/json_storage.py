import json
import logging
from typing import Optional, List

from models.product import Product
from .base_storage import IStorage

logger = logging.getLogger(__name__)

class JSONStorage(IStorage):
    
    def __init__(self, storage_path: str):
        self.output_path = storage_path
        self.products = self.load_existing_products()
    
    async def add(self, product: Product) -> None:
        try:
            self.products.append(product.dict())
            self._save_products()
        except Exception as e:
            logger.error(f"Error adding product {product.product_title}: {e}")
            raise RuntimeError(f"Failed to add product: {product.product_title}")

    async def update(self, product: Product) -> None:
        try:
            existing_product = await self.get(product.product_title)
            if existing_product:
                existing_product['product_price'] = product.product_price
                existing_product['path_to_image'] = product.path_to_image
            self._save_products()
        except Exception as e:
            logger.error(f"Error updating product {product.product_title}: {e}")
            raise RuntimeError(f"Failed to update product: {product.product_title}")

    async def get(self, product_title: str) -> Optional[dict]:
        try:
            for product in self.products:
                if product['product_title'] == product_title:
                    return product
            return None
        except Exception as e:
            return None

    def delete(self, product_title: str) -> None:
        pass

    def _save_products(self) -> None:
        try:
            with open(self.output_path, "w") as f:
                json.dump(self.products, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving products to storage: {e}")
            raise RuntimeError("Failed to save products to storage")

    def load_existing_products(self) -> List[dict]:
        try:
            with open(self.output_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return []
