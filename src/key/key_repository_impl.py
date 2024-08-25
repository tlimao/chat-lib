import json
from redis import Redis
from src.key.key import Key
from src.key.key_repository import KeyRepository


class KeyRepositoryImpl(KeyRepository):
    
    KEY_DIRECTORY: str = "chat:key"

    def __init__(self, redis_connection: Redis):
        self._redis_connection: Redis = redis_connection
    
    def save(self, key: Key) -> None:
        self._redis_connection.set(
            f"{self.KEY_DIRECTORY}:{key.id}",
            value=json.dumps(key.to_dict()))

    def get(self, key_id: str) -> Key:
        key_dict: dict = json.loads(self._redis_connection.get(
            f"{self.KEY_DIRECTORY}:{key_id}"))

        return Key.from_dict(key_dict)

    def update(self, key: Key) -> None:
        self.save(key)

    def delete(self, key_id: str) -> None:
        self._redis_connection.delete(f"{self.KEY_DIRECTORY}:{key_id}")