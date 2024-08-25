from src.message.envelope import Envelope
from src.message.error.message_not_deleted_error import MessageNotDeletedError
from src.message.error.message_not_updated_error import MessageNotUpdatedError
from src.message.message import Message
from src.message.message_repository import MessageRepository
from src.message.error.messages_not_delivered_error import MessagesNotDeliveredError
from src.message.error.messages_not_found_error import MessagesNotFoundError


class MessageManager:
    
    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository: MessageRepository = message_repository

    def get_messages(self, account_id: str) -> Envelope:
        try:
            messages: list[Message] = self._message_repository.get(account_id)
            
            return Envelope(messages=messages)
        except Exception as e:
            raise MessagesNotFoundError(f"Messages not found: {e}")

    def put_messages(self, envelope: Envelope) -> None:
        try:
           self._message_repository.save(envelope.messages)
        except Exception as e:
            print(e)
            raise MessagesNotDeliveredError(f"Messages not delivered: {e}")

    def delete_message(self, account_id: str, message_id: str) -> None:
        try:
            self._message_repository.delete(account_id=account_id, message_id=message_id)
        except Exception as e:
            raise MessageNotDeletedError(f"Message not deleted: {e}")

    def update_message(self, message: Message) -> None:
        try:
            self._message_repository.update(message)
        except Exception as e:
            raise MessageNotUpdatedError(f"Message not updated: {e}")