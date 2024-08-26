import uuid
from freedomlib.key.error.key_not_deleted_error import KeyNotDeletedError
from freedomlib.key.error.key_not_delivered_error import KeyNotDeliveredError
from freedomlib.key.error.key_not_found_error import KeyNotFoundError
from freedomlib.key.error.key_not_updated_error import KeyNotUpdatedError
from freedomlib.key.key import Key
from freedomlib.key.key_info import KeyInfo
from freedomlib.key.key_repository import KeyRepository


class KeyManager:
    
    def __init__(self, key_repository: KeyRepository) -> None:
        self._key_repository = key_repository

    def get_key(self, key_id: str) -> Key:
        try:            
            return self._key_repository.get(key_id)
        except Exception as e:
            raise KeyNotFoundError(f"Key not found: {e}")
        
    def get_account_key(self, account_id: str) -> Key:
        try:            
            return self._key_repository.get_key_by_account_id(account_id)
        except Exception as e:
            raise KeyNotFoundError(f"Key not found: {e}")

    def put_key(self, key_info: KeyInfo) -> Key:
        try:
            key: Key = Key(
                id=str(uuid.uuid4),
                account_id=key_info.account_id,
                pub_key=key_info.pub_key)
            
            self._key_repository.save(key)
            
            return key
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