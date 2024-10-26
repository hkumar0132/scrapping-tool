from pydantic import BaseModel

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
    path_to_image_public: str