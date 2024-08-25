from src.key.error.key_not_deleted_error import KeyNotDeletedError
from src.key.error.key_not_delivered_error import KeyNotDeliveredError
from src.key.error.key_not_found_error import KeyNotFoundError
from src.key.error.key_not_updated_error import KeyNotUpdatedError
from src.key.key import Key
from src.key.key_repository import KeyRepository


class KeyManager:
    
    def __init__(self, key_repository: KeyRepository) -> None:
        self._key_repository = key_repository

    def get_key(self, key_id: str) -> Key:
        try:            
            return self._key_repository.get(key_id)
        except Exception as e:
            raise KeyNotFoundError(f"Key not found: {e}")

    def put_key(self, key: Key) -> None:
        try:
           self._key_repository.save(key)
        except Exception as e:
            raise KeyNotDeliveredError(f"Key not delivered: {e}")

    def delete_key(self, key_id: str) -> None:
        try:
           self._key_repository.delete(key_id)
        except Exception as e:
            raise KeyNotDeletedError(f"Key not deleted: {e}")

    def update_key(self, key: Key) -> None:
        try:
           self._key_repository.save(key)
        except Exception as e:
            raise KeyNotUpdatedError(f"Key not updated: {e}")