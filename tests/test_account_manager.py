import pytest
from fakeredis import FakeRedis
from unittest.mock import MagicMock

from freedom.account.error.account_not_found_error import AccountNotFoundError
from freedom.account.account import Account
from freedom.account.account_info import AccountInfo
from freedom.account.account_manager import AccountManager
from freedom.account.account_repository import AccountRepository
from freedom.account.account_repository_impl import AccountRepositoryImpl
from freedom.account.error.account_not_created_error import AccountNotCreatedError

@pytest.fixture
def fake_redis():
    # Cria uma conexão fake do Redis usando fakeredis
    return FakeRedis()

@pytest.fixture
def mock_account_repository(fake_redis):
    # Passa a conexão fake do Redis para o SessionRepository
    return AccountRepositoryImpl(redis_connection=fake_redis)

@pytest.fixture
def account_manager(mock_account_repository):
    return AccountManager(mock_account_repository)

def test_create_account_success(account_manager: AccountManager):
    account_info: AccountInfo = AccountInfo(id="account1", nick="@account1")
        
    result: Account = account_manager.create_account(account_info=account_info)

    assert result.nick == account_info.nick

def test_create_account_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account_info: AccountInfo = AccountInfo(id="account1", nick="@account1")
    mock_account_repository.save = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(AccountNotCreatedError) as excinfo:
        account_manager.create_account(account_info=account_info)
    
    assert str(excinfo.value) == "Account not created: Redis error"

def test_get_account_success(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account: Account = Account(id="account1", nick="@account1")
    mock_account_repository.save(account)
    
    result: Account = account_manager.get_account(account_id=account.id)
    
    assert result.id == account.id

def test_get_account_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    mock_account_repository.get = MagicMock(side_effect=Exception("Redis Error"))
    
    with pytest.raises(AccountNotFoundError) as excinfo:
        account_manager.get_account("invalid_account_id")
    
    assert str(excinfo.value) == "Account not found: Redis Error"