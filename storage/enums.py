from enum import Enum


class StorageType(str, Enum):
    JSON = "json"
    MySQL = 'mysql'
    PostgreSQL = 'postgresql'
