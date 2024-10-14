from abc import ABC, abstractmethod
from freedomlib.account.account import Account


class AccountRepository(ABC):
    
    @abstractmethod
    def get_by_aci(self, aci: str) -> Account:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Account:
        ...

    @abstractmethod
    def get_by_phonenumber(self, phonenumber: str) -> Account:
        ...

    @abstractmethod
    def save(self, account: Account) -> Account:
        ...

    @abstractmethod
    def delete(self, aci: str) -> None:
        ...

    @abstractmethod
    def update(self, account: Account) -> Account:
        ...