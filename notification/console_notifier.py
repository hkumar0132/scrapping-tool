from notification.base_notifier import INotifier
import logging

logger = logging.getLogger(__name__)

class ConsoleNotifier(INotifier):
    
    def notify(self, message: str):
        logger.info(f"ConsoleNotifier: {message}")