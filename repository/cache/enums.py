from enum import Enum

class CacheType(str, Enum):
    REDIS = "redis"
    IN_MEMORY = "in_memory"