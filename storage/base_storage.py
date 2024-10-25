from typing import List, Optional
from models.product import Product

class IStorage:
    async def add(self, product: Product) -> None:
        pass

    async def update(self, product: Product) -> None:
        pass

    async def get(self, product_title: str) -> Optional[Product]:
        pass

    async def delete(self, product_title: str) -> None:
        pass