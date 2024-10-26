from .json_storage import JSONStorage
from .base_storage import IStorage
from .enums import StorageType

class StorageFactory:
    @staticmethod
    def get_storage(storage_type: StorageType, storage_path: str) -> IStorage:
        if storage_type == StorageType.JSON:
            return JSONStorage(storage_path)
        raise ValueError("Invalid storage type")
