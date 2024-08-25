import json
from redis import Redis

from src.message.message_repository import MessageRepository
from src.message.message import Message

class MessageRepositoryImpl(MessageRepository):
    
    MESSAGE_DIRECTORY: str = "chat:message"
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection
    
    def get(self, account_id: str) -> list[Message]:
        messages: list[Message] = []
                
        for key in self._redis_connection.scan_iter(f"{self.MESSAGE_DIRECTORY}:{account_id}:*"):
            message_data: dict = json.loads(self._redis_connection.get(key))
            messages.append(Message.from_dict(message_data))
                
        return messages

    def save(self, messages: list[Message]) -> None:
        for message in messages:
            self._redis_connection.set(
                f"{self.MESSAGE_DIRECTORY}:{message.sender_id}:{message.recipient_id}:{message.id}",
                json.dumps(message.to_dict()))

            self._redis_connection.set(
                f"{self.MESSAGE_DIRECTORY}:{message.recipient_id}:{message.sender_id}:{message.id}",
                json.dumps(message.to_dict()))

    def delete(self, account_id: str, message_id: str) -> None:
        message: Message = self._redis_connection.get(f"{self.MESSAGE_DIRECTORY}:{account_id}:{message_id}")
        
        self._redis_connection.delete(
            f"{self.MESSAGE_DIRECTORY}:{message.sender_id}:{message.recipient_id}:{message_id}")

        self._redis_connection.delete(
            f"{self.MESSAGE_DIRECTORY}:{message.recipient_id}:{message.sender_id}:{message_id}")

    def update(self, message: Message) -> Message:
        self.save([message])