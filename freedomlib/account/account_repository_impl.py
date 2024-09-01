import json

from redis import Redis
from freedomlib.account.account import Account
from freedomlib.account.account_repository import AccountRepository
from freedomlib.account.error.account_already_exists_error import AccountAlreadyExistsError
from freedomlib.account.error.account_not_found_error import AccountNotFoundError


class AccountRepositoryImpl(AccountRepository):
    
    ACCOUNT_DIRECTORY: str = "chat:account"

    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection = redis_connection
    
    def _get(self, key: str) -> Account:
        try:
            account_dict: dict = json.loads(self._redis_connection.get(key))

            return Account.from_dict(account_dict)
        except Exception:
            raise AccountNotFoundError(f"Account with key {key} not found")
    
    def get_by_id(self, account_id: str) -> Account:
        try:
            return self._get(f"{self.ACCOUNT_DIRECTORY}:id:{account_id}")
        except AccountNotFoundError:
            raise AccountNotFoundError(f"Account with id {account_id} not found")
    
    def get_by_email(self, email: str) -> Account:
        try:
            account_id: str = self._redis_connection.get(f"{self.ACCOUNT_DIRECTORY}:email:{email}").decode("utf-8")
            return self._get(f"{self.ACCOUNT_DIRECTORY}:id:{account_id}")
        except Exception:
            raise AccountNotFoundError(f"Account with email {email} not found")

    def get_by_phonenumber(self, phonenumber: str) -> Account:
        try:
            account_id: str = self._redis_connection.get(f"{self.ACCOUNT_DIRECTORY}:phonenumber:{phonenumber}").decode("utf-8")
            return self._get(f"{self.ACCOUNT_DIRECTORY}:id:{account_id}")
        except Exception:
            raise AccountNotFoundError(f"Account with phonenumber {phonenumber} not found")

    def save(self, account: Account) -> Account:
        try:
            self.get_by_phonenumber(account.phonenumber)
            raise AccountAlreadyExistsError("Account already exists!")
        except AccountNotFoundError:
            pass
        
        self._redis_connection.set(
            f"{self.ACCOUNT_DIRECTORY}:id:{account.id}",
            value=json.dumps(account.to_dict()))
        
        self._redis_connection.set(
            f"{self.ACCOUNT_DIRECTORY}:email:{account.email}",
            value=account.id)
        
        self._redis_connection.set(
            f"{self.ACCOUNT_DIRECTORY}:phonenumber:{account.phonenumber}",
            value=account.id)
        
        return account

    def delete(self, account_id: str) -> None:
        account: Account = self.get_by_id(account_id)
        self._redis_connection.delete(f"{self.ACCOUNT_DIRECTORY}:id:{account.id}")
        self._redis_connection.delete(f"{self.ACCOUNT_DIRECTORY}:email:{account.email}")
        self._redis_connection.delete(f"{self.ACCOUNT_DIRECTORY}:phonenumber:{account.phonenumber}")
        
    def update(self, account: Account) -> Account:
        return self.save(account)