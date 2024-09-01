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
from freedomlib.account.error.account_already_exists_error import AccountAlreadyExistsError

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
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com", phonenumber="1234567890")
        
    account: Account = account_manager.create_account(account_info=account_info)

    assert account.nick == account_info.nick
    assert account.email == account_info.email
    assert account.phonenumber == account_info.phonenumber

def test_create_account_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com", phonenumber="1234567890")
    account_manager.create_account(account_info=account_info)
    
    with pytest.raises(AccountNotCreatedError) as excinfo:
        account_manager.create_account(account_info=account_info)
    
    assert isinstance(excinfo.value, AccountNotCreatedError)

def test_get_account_success(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account: Account = Account(id="account1", nick="@account1", email="account1@mail.com", phonenumber="1234567890")
    mock_account_repository.save(account)
    
    result: Account = account_manager.get_account_by_id(account_id=account.id)
    
    assert result.id == account.id
    assert result.nick == account.nick
    assert result.email == account.email
    assert result.phonenumber == account.phonenumber

def test_get_account_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):    
    with pytest.raises(AccountNotFoundError) as excinfo:
        account_manager.get_account_by_id("invalid_key")
    
    assert isinstance(excinfo.value, AccountNotFoundError)
    assert str(excinfo.value) == "Account not found: Account with id invalid_key not found"

def test_get_account_by_email_success(account_manager: AccountManager):
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com", phonenumber="1234567890")
    account_manager.create_account(account_info)
    
    result: Account = account_manager.get_account_by_email(email=account_info.email)
    
    assert result.nick == account_info.nick
    assert result.email == account_info.email
    assert result.phonenumber == account_info.phonenumber

def test_get_account_by_email_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    with pytest.raises(AccountNotFoundError) as excinfo:
        account_manager.get_account_by_email("invalid_email")
    
    assert isinstance(excinfo.value, AccountNotFoundError)
    assert str(excinfo.value) == "Account not found: Account with email invalid_email not found"

def test_create_account_exists_failure(account_manager: AccountManager, mock_account_repository: AccountRepository):
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com", phonenumber="1234567890")
    account_manager.create_account(account_info)
    
    with pytest.raises(AccountNotCreatedError) as excinfo:
        account_manager.create_account(account_info=account_info)
    
    assert isinstance(excinfo.value, AccountNotCreatedError)
    assert str(excinfo.value) == "Account not created: Account already exists!"