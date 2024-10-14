from freedomlib.contact.contact import Contact
from abc import ABC, abstractmethod

class ContactRepository(ABC):

    @abstractmethod
    def get_by_phonenumber(self, phonenumber: str) -> Contact:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Contact:
        pass
    
    @abstractmethod
    def save(self, contact: Contact) -> Contact:
        pass
    
    @abstractmethod
    def delete(self, aci: str) -> None:
        pass

    @abstractmethod
    def update(self, contact: Contact) -> Contact:
        pass