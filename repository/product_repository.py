from typing import List

from abc import ABC, abstractmethod
from models.product import Product

class IProductRepository(ABC):
    
    @abstractmethod
    async def sync_products(self, products: List[Product]) -> None:
        pass

    @abstractmethod
    async def sync_single_product(self, product: Product) -> None:
        pass
