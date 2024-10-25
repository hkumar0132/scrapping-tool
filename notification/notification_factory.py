from notification.console_notifier import ConsoleNotifier
from notification.base_notifier import INotifier
from .enums import NotifierType

class NotificationFactory:
    @staticmethod
    def get_notifier(notification_type: NotifierType) -> INotifier:
        if notification_type == NotifierType.CONSOLE:
            return ConsoleNotifier()
        raise ValueError("Invalid notifier type")