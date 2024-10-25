from pydantic import BaseModel, HttpUrl, validator
from typing import Optional

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScrapeSettings(BaseModel):
    limit: Optional[int] = None
    proxy: Optional[HttpUrl] = None