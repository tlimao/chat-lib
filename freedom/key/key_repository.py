from abc import ABC, abstractmethod

from freedom.key.key import Key


class KeyRepository(ABC):
    
    @abstractmethod
    def save(self, key: Key) -> None:
        ...

    @abstractmethod
    def get(self, account_id: str) -> Key:
        ...

    @abstractmethod
    def update(self, key: Key) -> None:
        ...

    @abstractmethod
    def delete(self, key_id: str) -> None:
        ...