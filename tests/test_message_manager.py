from datetime import datetime
import pytest
import uuid
from fakeredis import FakeRedis
from unittest.mock import MagicMock

from freedomlib.message.envelope import Envelope
from freedomlib.message.error.messages_not_delivered_error import MessagesNotDeliveredError
from freedomlib.message.error.messages_not_found_error import MessagesNotFoundError
from freedomlib.message.error.message_not_deleted_error import MessageNotDeletedError
from freedomlib.message.message import Message
from freedomlib.message.message_manager import MessageManager
from freedomlib.message.message_repository_impl import MessageRepositoryImpl

@pytest.fixture
def fake_redis():
    # Cria uma conexão fake do Redis usando fakeredis
    return FakeRedis()

@pytest.fixture
def mock_message_repository(fake_redis):
    # Passa a conexão fake do Redis para o SessionRepository
    return MessageRepositoryImpl(redis_connection=fake_redis)

@pytest.fixture
def message_manager(mock_message_repository):
    return MessageManager(mock_message_repository)

def test_get_messages_success(message_manager: MessageManager, mock_message_repository: MessageRepositoryImpl):
    message: Message = Message(
        id=str(uuid.uuid4()),
        sender_id="account1",
        recipient_id="account2", 
        timestamp=int(datetime.now().timestamp()),
        nonce=bytearray(12),
        tag=bytearray(12),
        cipher_message=bytearray(12))
    
    mock_message_repository.save([message])
    
    result: Envelope = message_manager.get_messages("account1")
    
    assert result.messages[0].sender_id == message.sender_id
    assert result.messages[0].recipient_id == message.recipient_id
    assert result.messages[0].timestamp == message.timestamp
    assert result.messages[0].nonce == message.nonce
    assert result.messages[0].tag == message.tag
    assert result.messages[0].cipher_message == message.cipher_message
    
def test_get_messages_failure(message_manager: MessageManager, mock_message_repository: MessageRepositoryImpl):
    mock_message_repository.get = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(MessagesNotFoundError) as excinfo:
        message_manager.get_messages("account_id")
    
    assert str(excinfo.value) == "Messages not found: Redis error"

def test_put_messages_success(message_manager: MessageManager, mock_message_repository: MessageRepositoryImpl):
    message: Message = Message(
        id=str(uuid.uuid4()),
        sender_id="account1",
        recipient_id="account2", 
        timestamp=int(datetime.now().timestamp()),
        nonce=bytearray(12),
        tag=bytearray(12),
        cipher_message=bytearray(12))
    
    envelope: Envelope = Envelope(messages=[message])

    message_manager.put_messages(envelope)
    
    result: Envelope = message_manager.get_messages("account1")
    
    assert result.messages[0].sender_id == message.sender_id
    assert result.messages[0].recipient_id == message.recipient_id
    assert result.messages[0].timestamp == message.timestamp
    assert result.messages[0].nonce == message.nonce
    assert result.messages[0].tag == message.tag
    assert result.messages[0].cipher_message == message.cipher_message

def test_put_messages_failure(message_manager: MessageManager, mock_message_repository: MessageRepositoryImpl):
    message: Message = Message(
        id=str(uuid.uuid4()),
        sender_id="account1",
        recipient_id="account2", 
        timestamp=int(datetime.now().timestamp()),
        nonce=bytearray(12),
        tag=bytearray(12),
        cipher_message=bytearray(12))
    
    envelope: Envelope = Envelope(messages=[message])
    
    mock_message_repository.save = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(MessagesNotDeliveredError) as excinfo:
        message_manager.put_messages(envelope)
    
    assert isinstance(excinfo.value, MessagesNotDeliveredError)

def test_delete_message_success(message_manager: MessageManager, mock_message_repository: MessageRepositoryImpl):
    message: Message = Message(
        id=str(uuid.uuid4()),
        sender_id="account1",
        recipient_id="account2", 
        timestamp=int(datetime.now().timestamp()),
        nonce=bytearray(12),
        tag=bytearray(12),
        cipher_message=bytearray(12))
    
    envelope: Envelope = Envelope(messages=[message])

    message_manager.put_messages(envelope)

    envelope: Envelope = message_manager.get_messages(message.sender_id)

    assert len(envelope.messages) == 1

    message_manager.delete_message(message.sender_id, message.id)

    envelope: Envelope = message_manager.get_messages(message.sender_id)

    assert len(envelope.messages) == 0

def test_delete_message_failure(message_manager: MessageManager, mock_message_repository: MessageRepositoryImpl):
    message: Message = Message(
        id=str(uuid.uuid4()),
        sender_id="account1",
        recipient_id="account2", 
        timestamp=int(datetime.now().timestamp()),
        nonce=bytearray(12),
        tag=bytearray(12),
        cipher_message=bytearray(12))
    
    envelope: Envelope = Envelope(messages=[message])

    message_manager.put_messages(envelope)

    envelope: Envelope = message_manager.get_messages(message.sender_id)

    assert len(envelope.messages) == 1

    mock_message_repository.delete = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(MessageNotDeletedError) as excinfo:
        message_manager.delete_message(message.sender_id, message.id)
    
    assert isinstance(excinfo.value, MessageNotDeletedError)

def test_delete_message_for_me_success(message_manager: MessageManager, mock_message_repository: MessageRepositoryImpl):
    message: Message = Message(
        id=str(uuid.uuid4()),
        sender_id="account1",
        recipient_id="account2", 
        timestamp=int(datetime.now().timestamp()),
        nonce=bytearray(12),
        tag=bytearray(12),
        cipher_message=bytearray(12))
    
    envelope: Envelope = Envelope(messages=[message])

    message_manager.put_messages(envelope)

    envelope: Envelope = message_manager.get_messages(message.sender_id)

    assert len(envelope.messages) == 1

    message_manager.delete_message(message.sender_id, message.id)

    envelope: Envelope = message_manager.get_messages(message.sender_id)

    assert len(envelope.messages) == 0