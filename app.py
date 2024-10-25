import logging
from fastapi import FastAPI, Depends, HTTPException
from models.product import ScrapeSettings
from config import Config
from scrapper.scraper_factory import ScraperFactory
from scrapper.enums import ScrapperType
from storage.storage_factory import StorageFactory
from storage.enums import StorageType
from cache.cache_factory import CacheFactory
from cache.enums import CacheType
from notification.notification_factory import NotificationFactory
from notification.enums import NotifierType
from product.product_manager import ProductManager
from services.image_downloader import ImageDownloader

import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI()

def token_auth(token: str):
    if token != Config.SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")

@app.post("/scrape/")
async def scrape(settings: ScrapeSettings, token: str = Depends(token_auth)):

    try:

        cache_factory = CacheFactory()
        cache = cache_factory.get_cache(CacheType.REDIS)
        storage_factory = StorageFactory()
        storage = storage_factory.get_storage(StorageType.JSON, storage_path=os.path.join(os.getcwd(), f"{Config.OUTPUT_FOLDER}/products.json"))
        image_downloader = ImageDownloader(os.path.join(os.getcwd(), f"{Config.OUTPUT_FOLDER}/images"))
        product_manager = ProductManager(cache, storage, image_downloader)

        scraper_factory = ScraperFactory()
        scraper = scraper_factory.get_scraper(ScrapperType.WEB, settings, product_manager, url=Config.WEBSITE_URL, proxy=settings.proxy)

        console_notifier = NotificationFactory().get_notifier(NotifierType.CONSOLE)

        scraper.attach(console_notifier)
        await scraper.scrape()

        return {"message": f"Scraped products successfully."}

    except HTTPException as http_exc:
        logger.error(f"HTTP error: {http_exc.detail}")
        raise
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")