import requests
from bs4 import BeautifulSoup
from typing import List
from models.product import Product, ScrapeSettings
from scrapper.base_scrapper import IScrapper
from product.product_manager import ProductManager
from notification.base_notifier import INotifier

from utils.retry import retry
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScrapper(IScrapper):
    
    def __init__(self, settings: ScrapeSettings, product_manager: ProductManager, url: str, proxy: str = None):
        self.url = url
        self.settings = settings
        self.product_manager = product_manager
        self._observers : List[INotifier] = []
        self.proxy = proxy

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self, message: str):
        for observer in self._observers:
            observer.notify(message)

    @retry
    def fetch_page(self, page_number: int) -> str:
        try:
            if page_number == 1:
                url = self.url
            else:
                url = f"{self.url}/page/{page_number}"
                
            response = requests.get(url, proxies={
                'http': self.proxy
            })
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {page_number}: {str(e)}")
            raise RuntimeError(f"Error fetching page {page_number}: {str(e)}") from e

    def __parse_products(self, html: str) -> List[Product]:
        try:
            soup = BeautifulSoup(html, "html.parser")
            products = []

            for product_div in soup.select(".product"):
                title = product_div.select_one(".woo-loop-product__title").text.strip()

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
                products.append(Product(product_title=title, product_price=discounted_price, path_to_image=img_url))

            return products
        except AttributeError as e:
            logger.error(f"Failed to parse products from HTML: {str(e)}")
            raise RuntimeError(f"Error parsing products from HTML: {str(e)}") from e
        except ValueError as e:
            logger.error(f"Failed to convert product price to float: {str(e)}")
            raise RuntimeError(f"Invalid price format encountered: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error while parsing products: {str(e)}")
            raise RuntimeError(f"Unexpected error during parsing: {str(e)}") from e

    async def scrape(self):
        
        # Keeping this sync as there is a rate limit on the
        # website to be scrapped

        for page in range(1, self.settings.limit + 1):
            try:
                logger.info(f"\n\nScraping page {page}...")
                html = self.fetch_page(page)
                products = self.__parse_products(html)

                logger.info(f"\nSyncing page {page} with storage...")
                await self.product_manager.sync_products(products)

                logger.info(f"\nPage {page} scraped successfully")

            except RuntimeError as e:
                logger.error(f"Scraping failed with runtime error on page {page}: {str(e)}")
            except Exception as e:
                logger.error(f"Scraping failed due to an unexpected error on page {page}: {str(e)}")

        self._notify(f"Scraping completed successfully for {self.settings.limit} pages.")                