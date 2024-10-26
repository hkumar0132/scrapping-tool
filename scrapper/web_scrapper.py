import requests
from typing import List
from models.scrape_settings import ScrapeSettings
from scrapper.base_scrapper import IScrapper
from repository.product_repository import IProductRepository
from notification.base_notifier import INotifier
from .page_fetcher import PageFetcher
from .product_parser import ProductParser

import logging

logger = logging.getLogger(__name__)

class WebScrapper(IScrapper):
    
    def __init__(self, settings: ScrapeSettings, product_repo_manager: IProductRepository, fetcher: PageFetcher, parser: ProductParser, url: str, proxy: str):
        self.url = url
        self.settings = settings
        self.product_repo_manager = product_repo_manager
        self._observers: List[INotifier] = []
        self.fetcher = fetcher
        self.parser = parser
        self.proxy = proxy
            
    def attach(self, observer: INotifier):
        self._observers.append(observer)

    def detach(self, observer: INotifier):
        self._observers.remove(observer)

    def _notify(self, message: str):
        for observer in self._observers:
            observer.notify(message)

    async def scrape(self):
        
        # Keeping this sync as there is a rate limit on the
        # website to be scrapped

        try:
            for page in range(1, self.settings.limit + 1):
                logger.info(f"\n\nScraping page {page}...")
                html = self.fetcher.fetch_page(page)
                products = self.parser.parse_products(html)

                logger.info(f"\nSyncing page {page} with storage...")
                await self.product_repo_manager.sync_products(products)

                logger.info(f"\nPage {page} scraped successfully")
        except Exception as e:
            logger.error(f"Scraping failed due to an unexpected error on page {page}: {str(e)}")
            raise e

        self._notify(f"Scraping completed successfully for {self.settings.limit} pages.")                