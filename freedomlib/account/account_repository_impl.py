import json

from redis import Redis
from freedomlib.account.account import Account
from freedomlib.account.account_repository import AccountRepository
from freedomlib.account.error.account_already_exists_error import AccountAlreadyExistsError


class AccountRepositoryImpl(AccountRepository):
    
    ACCOUNT_DIRECTORY: str = "chat:account"

    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection = redis_connection
    
    def get(self, account_id: str) -> Account:
        account_dict: dict = json.loads(self._redis_connection.get(f"{self.ACCOUNT_DIRECTORY}:id:{account_id}"))

        return Account.from_dict(account_dict)
    
    def get_by_email(self, email: str) -> Account:
        account_id: str = self._redis_connection.get(f"{self.ACCOUNT_DIRECTORY}:email:{email}").decode()
        return self.get(account_id)
    
    def _exists(self, email: str) -> bool:
        return self._redis_connection.get(f"{self.ACCOUNT_DIRECTORY}:email:{email}") != None

    def save(self, account: Account) -> Account:
        if (self._exists(account.email)): raise AccountAlreadyExistsError("Account already exists!")
        
        self._redis_connection.set(
            f"{self.ACCOUNT_DIRECTORY}:id:{account.id}",
            value=json.dumps(account.to_dict()))
        
        self._redis_connection.set(
            f"{self.ACCOUNT_DIRECTORY}:email:{account.email}",
            value=account.id)
        
        return account

    def delete(self, account_id: str) -> None:
        account: Account = self.get(account_id)
        self._redis_connection.delete(f"{self.ACCOUNT_DIRECTORY}:id:{account.id}")
        self._redis_connection.delete(f"{self.ACCOUNT_DIRECTORY}:email:{account.email}")

    def update(self, account: Account) -> Account:
        return self.save(account)