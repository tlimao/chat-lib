from abc import ABC
from freedomlib.message.message import Message


class MessageRepository(ABC):
    
    def save(self, messages: list[Message]) -> None:
        raise NotImplementedError()

    def save_with_expiration(self, messages: list[Message], expiration: int) -> None:
        raise NotImplementedError()
    
    def get(self, aci: str) -> list[Message]:
        raise NotImplementedError()

    def delete(self, aci: str, message_id: str) -> None:
        raise NotImplementedError()

    def delete_for_me(self, aci: str, message_id: str) -> None:
        raise NotImplementedError()

    def update(self, message: Message) -> Message:
        raise NotImplementedError()