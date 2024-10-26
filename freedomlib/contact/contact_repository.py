from freedomlib.contact.contact import Contact
from abc import ABC, abstractmethod

class ContactRepository(ABC):

    @abstractmethod
    def get_by_phonenumber(self, phonenumber: str) -> Contact:
        raise NotImplementedError()

    @abstractmethod
    def get_by_email(self, email: str) -> Contact:
        raise NotImplementedError()
    
    @abstractmethod
    def save(self, contact: Contact) -> Contact:
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, aci: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self, contact: Contact) -> Contact:
        raise NotImplementedError()