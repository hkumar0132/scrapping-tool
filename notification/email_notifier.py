from notification.base_notifier import INotifier

class EmailNotifier(INotifier):
    def notify(self, message: str):
        print(f"Email notification: {message}")
