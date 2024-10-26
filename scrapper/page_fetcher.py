import requests
from utils.retry import retry
from exceptions.network_error import NetworkError
import logging

logger = logging.getLogger(__name__)

class PageFetcher:
    def __init__(self, base_url: str, proxy: str = None):
        self.base_url = base_url
        self.proxy = proxy

    @retry
    def fetch_page(self, page_number: int) -> str:
        try:
            url = self.base_url if page_number == 1 else f"{self.base_url}/page/{page_number}"
            response = requests.get(url, proxies={'http': self.proxy} if self.proxy else None)
            response.raise_for_status()
            return response.text
        except requests.ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise NetworkError(f"Network error: {str(e)}") from e
        except requests.Timeout as e:
            logger.error(f"Timeout error: {str(e)}")
            raise NetworkError(f"Network error (timeout): {str(e)}") from e
        except requests.RequestException as e:
            logger.error(f"General request error: {str(e)}")
            raise RuntimeError(f"Request error: {str(e)}") from e
