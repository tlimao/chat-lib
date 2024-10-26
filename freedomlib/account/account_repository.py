from abc import ABC, abstractmethod
from freedomlib.account.account import Account


class AccountRepository(ABC):
    
    @abstractmethod
    def get_by_aci(self, aci: str) -> Account:
        raise NotImplementedError()

    @abstractmethod
    def get_by_email(self, email: str) -> Account:
        raise NotImplementedError()

    @abstractmethod
    def get_by_phonenumber(self, phonenumber: str) -> Account:
        raise NotImplementedError()

    @abstractmethod
    def save(self, account: Account) -> Account:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, aci: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self, account: Account) -> Account:
        raise NotImplementedError()