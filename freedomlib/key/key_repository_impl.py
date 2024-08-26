import json
from redis import Redis
from freedomlib.key.key import Key
from freedomlib.key.key_repository import KeyRepository


class KeyRepositoryImpl(KeyRepository):
    
    KEY_DIRECTORY: str = "chat:key"

    def __init__(self, redis_connection: Redis):
        self._redis_connection: Redis = redis_connection
    
    def save(self, key: Key) -> None:
        self._redis_connection.set(
            f"{self.KEY_DIRECTORY}:id:{key.id}",
            value=json.dumps(key.to_dict()))

        self._redis_connection.set(
            f"{self.KEY_DIRECTORY}:account:{key.account_id}",
            value=key.id)

    def get(self, key_id: str) -> Key:
        key_dict: dict = json.loads(self._redis_connection.get(f"{self.KEY_DIRECTORY}:id:{key_id}"))

        return Key.from_dict(key_dict)

    def get_key_by_account_id(self, account_id: str) -> Key:
        key_id: str = self._redis_connection.get(f"{self.KEY_DIRECTORY}:account:{account_id}").decode()
        
        return self.get(key_id)

    def update(self, key: Key) -> None:
        self.save(key)

    def delete(self, key_id: str) -> None:
        self._redis_connection.delete(f"{self.KEY_DIRECTORY}:{key_id}")