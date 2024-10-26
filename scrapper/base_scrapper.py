from abc import ABC, abstractmethod
from notification.base_notifier import INotifier

class IScrapper(ABC):

    @abstractmethod
    def attach(self, observer: INotifier):
        pass

    @abstractmethod
    def detach(self, observer: INotifier):
        pass
    
    @abstractmethod
    async def scrape(self) -> list:
        pass
