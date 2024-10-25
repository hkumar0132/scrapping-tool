from enum import Enum

class NotifierType(str, Enum):
    CONSOLE = "console"
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    SMS = "sms"