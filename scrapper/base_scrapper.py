from abc import ABC, abstractmethod
from models.product import ScrapeSettings

class IScrapper(ABC):

    @abstractmethod
    def attach(self):
        pass

    @abstractmethod
    def detach(self):
        pass
    
    @abstractmethod
    async def scrape(self) -> list:
        pass
