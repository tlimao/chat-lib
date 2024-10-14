from abc import ABC
from freedomlib.message.message import Message


class MessageRepository(ABC):
    
    def save(self, messages: list[Message]) -> None:
        ...

    def save_with_expiration(self, messages: list[Message], expiration: int) -> None:
        ...
    
    def get(self, aci: str) -> list[Message]:
        ...

    def delete(self, aci: str, message_id: str) -> None:
        ...

    def delete_for_me(self, aci: str, message_id: str) -> None:
        ...

    def update(self, message: Message) -> Message:
        ...