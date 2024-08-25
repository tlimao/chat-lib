import json

from redis import Redis
from freedomlib.account.account import Account
from freedomlib.account.account_repository import AccountRepository


class AccountRepositoryImpl(AccountRepository):
    
    ACCOUNT_DIRECTORY: str = "chat:account"

    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection = redis_connection
    
    def get(self, account_id: str) -> Account:
        account_dict: dict = json.loads(self._redis_connection.get(f"{self.ACCOUNT_DIRECTORY}:{account_id}"))

        return Account.from_dict(account_dict)

    def save(self, account: Account) -> None:
        self._redis_connection.set(
            f"{self.ACCOUNT_DIRECTORY}:{account.id}",
            value=json.dumps(account.to_dict())
        )

    def delete(self, account_id: str) -> None:
        self._redis_connection.delete(f"{self.ACCOUNT_DIRECTORY}:{account_id}")

    def update(self, account: Account) -> Account:
        self._redis_connection.set(
            f"{self.ACCOUNT_DIRECTORY}:{account.id}",
            value=json.dumps(account.to_dict())
        )
        
        return account