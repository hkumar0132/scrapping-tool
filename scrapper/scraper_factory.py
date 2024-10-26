from scrapper.web_scrapper import WebScrapper
from models.scrape_settings import ScrapeSettings
from scrapper.base_scrapper import IScrapper
from repository.product_repository import IProductRepository
from .enums import ScrapperType
from scrapper.page_fetcher import PageFetcher
from scrapper.product_parser import ProductParser

class ScraperFactory:
    @staticmethod
    def get_scraper(scrapper_type: ScrapperType, settings: ScrapeSettings, product_repo_manager: IProductRepository, url: str, proxy: str) -> IScrapper:
        if scrapper_type == ScrapperType.WEB:
            fetcher = PageFetcher(url, proxy) 
            parser = ProductParser()

            return WebScrapper(settings, product_repo_manager, fetcher, parser, url, proxy)
        
        raise ValueError("Invalid scrapper type")
