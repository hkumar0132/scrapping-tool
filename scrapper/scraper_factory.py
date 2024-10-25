from scrapper.web_scrapper import WebScrapper
from models.product import ScrapeSettings
from scrapper.base_scrapper import IScrapper
from product.product_manager import ProductManager
from .enums import ScrapperType

class ScraperFactory:
    @staticmethod
    def get_scraper(scrapper_type: ScrapperType, settings: ScrapeSettings, product_manager: ProductManager, url: str, proxy: str) -> IScrapper:
        if scrapper_type == ScrapperType.WEB:
            return WebScrapper(settings, product_manager, url, proxy)
        raise ValueError("Invalid scrapper type")