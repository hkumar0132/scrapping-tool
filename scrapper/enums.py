from enum import Enum

class ScrapperType(str, Enum):
    WEB = "web"
    API = "api"
    DATABASE = "database"