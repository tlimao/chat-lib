import pytest
from fakeredis import FakeRedis
from unittest.mock import MagicMock

from freedomlib.account.error.account_not_found_error import AccountNotFoundError
from freedomlib.account.account import Account
from freedomlib.account.account_info import AccountInfo
from freedomlib.account.account_manager import AccountManager
from freedomlib.account.account_repository import AccountRepository
from freedomlib.account.account_repository_impl import AccountRepositoryImpl
from freedomlib.account.error.account_not_created_error import AccountNotCreatedError

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
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com")
        
    account: Account = account_manager.create_account(account_info=account_info)

    assert account.nick == account_info.nick
    assert account.email == account_info.email

def test_create_account_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com")
    mock_account_repository.save = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(AccountNotCreatedError) as excinfo:
        account_manager.create_account(account_info=account_info)
    
    assert str(excinfo.value) == "Account not created: Redis error"

def test_get_account_success(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account: Account = Account(id="account1", nick="@account1", email="account1@mail.com")
    mock_account_repository.save(account)
    
    result: Account = account_manager.get_account(account_id=account.id)
    
    assert result.id == account.id
    assert result.nick == account.nick
    assert result.email == account.email

def test_get_account_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    mock_account_repository.get = MagicMock(side_effect=Exception("Redis Error"))
    
    with pytest.raises(AccountNotFoundError) as excinfo:
        account_manager.get_account("invalid_account_id")
    
    assert str(excinfo.value) == "Account not found: Redis Error"

def test_get_account_by_email_success(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account: Account = Account(id="account1", nick="@account1", email="account1@mail.com")
    mock_account_repository.save(account)
    
    result: Account = account_manager.get_account_by_email(email=account.email)
    
    assert result.id == account.id
    assert result.nick == account.nick
    assert result.email == account.email

def test_get_account_by_email_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    mock_account_repository.get_by_email = MagicMock(side_effect=Exception("Redis Error"))
    
    with pytest.raises(AccountNotFoundError) as excinfo:
        account_manager.get_account_by_email("invalid_email")
    
    assert str(excinfo.value) == "Account not found: Redis Error"

def test_create_account_exists_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com")
    account_manager.create_account(account_info)
    
    with pytest.raises(AccountNotCreatedError) as excinfo:
        account_manager.create_account(account_info=account_info)
    
    assert str(excinfo.value) == "Account not created: Account already exists!"