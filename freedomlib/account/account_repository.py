from abc import ABC
from freedomlib.account.account import Account


class AccountRepository(ABC):
    
    def get(self, account_id: str) -> Account:
        ...

    def get_by_email(self, email: str) -> Account:
        ...

    def save(self, account: Account) -> Account:
        ...

    def delete(self, account_id: str) -> None:
        ...

    def update(self, account: Account) -> Account:
        ...