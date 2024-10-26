from typing import Optional

from models.product import Product

class ICache:

    async def get(self, key: str) -> Optional[dict]:
        pass

    async def add(self, key: str, product: Product) -> None:
        pass

    async def update(self, key: str, product: Product) -> None:
        pass

    async def delete(self, key: str) -> None:
        pass