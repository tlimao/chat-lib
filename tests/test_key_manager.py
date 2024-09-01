import pytest
from fakeredis import FakeRedis
from unittest.mock import MagicMock

from freedomlib.key.error.key_not_delivered_error import KeyNotDeliveredError
from freedomlib.key.error.key_not_found_error import KeyNotFoundError
from freedomlib.key.key import Key
from freedomlib.key.key_info import KeyInfo
from freedomlib.key.key_manager import KeyManager
from freedomlib.key.key_repository import KeyRepository
from freedomlib.key.key_repository_impl import KeyRepositoryImpl


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
    key_info: KeyInfo = KeyInfo(account_id="account1", pub_key="------BEGIN KEY ------- .....")
        
    key: Key = key_manager.put_key(key_info)
    
    result: Key = key_manager.get_key_by_id(key.id)

    assert result.account_id == key.account_id
    assert result.pub_key == key.pub_key
    assert result.id == key.id

def test_put_key_failure(key_manager: KeyManager, mock_key_repository: KeyRepository):
    key_info: KeyInfo = KeyInfo(account_id="account1", pub_key="------BEGIN KEY ------- .....")
    
    mock_key_repository.save = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(KeyNotDeliveredError) as excinfo:
        key_manager.put_key(key_info=key_info)
    
    assert str(excinfo.value) == "Key not delivered: Redis error"

def test_get_key_success(key_manager: KeyManager, mock_key_repository: KeyRepository):
    key: Key = Key(account_id="account1", id="key1", pub_key="------BEGIN KEY ------- .....")
    mock_key_repository.save(key)
    
    result: Key = key_manager.get_key_by_id(key.id)
    
    assert result.id == key.id
    
def test_get_account_key_success(key_manager: KeyManager, mock_key_repository: KeyRepository):
    key: Key = Key(account_id="account1", id="key1", pub_key="------BEGIN KEY ------- .....")
    mock_key_repository.save(key)
    
    result: Key = key_manager.get_account_key(key.account_id)
    
    assert result.id == key.id

def test_get_key_failure(key_manager: KeyManager, mock_key_repository: KeyRepository):
    mock_key_repository.get = MagicMock(side_effect=Exception("Redis Error"))
    
    with pytest.raises(KeyNotFoundError) as excinfo:
        key_manager.get_key_by_id("invalid_key_id")
    
    assert str(excinfo.value) == "Key not found: Redis Error"

def test_get__account_key_failure(key_manager: KeyManager, mock_key_repository: KeyRepository):
    mock_key_repository.get_key_by_account_id = MagicMock(side_effect=Exception("Redis Error"))
    
    with pytest.raises(KeyNotFoundError) as excinfo:
        key_manager.get_account_key("invalid_key_id")
    
    assert str(excinfo.value) == "Key not found: Redis Error"