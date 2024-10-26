from bs4 import BeautifulSoup
from typing import List
import logging

from models.product import Product
from exceptions.parsing_error import ParsingError

logger = logging.getLogger(__name__)

class ProductParser:
    @staticmethod
    def parse_products(html: str) -> List[Product]:
        try:
            soup = BeautifulSoup(html, "html.parser")
            products = []

            for product_div in soup.select(".product"):
                title = None
                title_div = product_div.select_one(".woo-loop-product__title")
                if title_div:
                    title = title_div.text.strip()
                else:
                    logger.warning("Product title not found")
                    continue

                price_div = product_div.select_one(".price")
                if price_div:
                    prices = price_div.text.strip().split('₹')
                    if len(prices) == 3:
                        discounted_price = float(prices[1].strip())
                    elif len(prices) == 2:
                        discounted_price = float(prices[1].strip())
                    else:
                        discounted_price = "N/A"
                img_url = product_div.select("img")[0].get("data-lazy-src")
                products.append(Product(product_title=title, product_price=discounted_price, path_to_image_public=img_url, path_to_image=''))

            return products
        except AttributeError as e:
            logger.error(f"Failed to parse products from HTML: {str(e)}")
            raise ParsingError(f"Error parsing products from HTML: {str(e)}") from e
        except ValueError as e:
            logger.error(f"Failed to convert product price to float: {str(e)}")
            raise ParsingError(f"Invalid price format encountered: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error while parsing products: {str(e)}")
            raise ParsingError(f"Unexpected error during parsing: {str(e)}") from e
