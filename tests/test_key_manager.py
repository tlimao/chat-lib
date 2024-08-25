import pytest
from fakeredis import FakeRedis
from unittest.mock import MagicMock

from freedom.key.error.key_not_delivered_error import KeyNotDeliveredError
from freedom.key.error.key_not_found_error import KeyNotFoundError
from freedom.key.key import Key
from freedom.key.key_manager import KeyManager
from freedom.key.key_repository import KeyRepository
from freedom.key.key_repository_impl import KeyRepositoryImpl


@pytest.fixture
def fake_redis():
    # Cria uma conexão fake do Redis usando fakeredis
    return FakeRedis()

@pytest.fixture
def mock_key_repository(fake_redis):
    # Passa a conexão fake do Redis para o SessionRepository
    return KeyRepositoryImpl(redis_connection=fake_redis)

@pytest.fixture
def key_manager(mock_key_repository):
    return KeyManager(mock_key_repository)

def test_put_key_success(key_manager: KeyManager):
    key: Key = Key(account_id="account1", id="key1", pub_key="------BEGIN KEY ------- .....")
        
    key_manager.put_key(key)
    
    result: Key = key_manager.get_key("key1")

    assert result.account_id == key.account_id
    assert result.id == key.id
    assert result.pub_key == key.pub_key

def test_put_key_failure(key_manager: KeyManager, mock_key_repository: KeyRepository):
    key: Key = Key(account_id="account1", id="key1", pub_key="------BEGIN KEY ------- .....")
    
    mock_key_repository.save = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(KeyNotDeliveredError) as excinfo:
        key_manager.put_key(key=key)
    
    assert str(excinfo.value) == "Key not delivered: Redis error"

def test_get_key_success(key_manager: KeyManager, mock_key_repository: KeyRepository):
    key: Key = Key(account_id="account1", id="key1", pub_key="------BEGIN KEY ------- .....")
    mock_key_repository.save(key)
    
    result: Key = key_manager.get_key(key.id)
    
    assert result.id == key.id

def test_get_key_failure(key_manager: KeyManager, mock_key_repository: KeyRepository):
    mock_key_repository.get = MagicMock(side_effect=Exception("Redis Error"))
    
    with pytest.raises(KeyNotFoundError) as excinfo:
        key_manager.get_key("invalid_key_id")
    
    assert str(excinfo.value) == "Key not found: Redis Error"