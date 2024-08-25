from abc import ABC
from freedom.account.account import Account


class AccountRepository(ABC):
    
    def get(self, account_id: str) -> Account:
        ...

    def save(self, account: Account) -> None:
        ...

    def delete(self, account_id: str) -> None:
        ...

    def update(self, account: Account) -> Account:
        ...