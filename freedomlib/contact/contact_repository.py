from freedomlib.contact.contact import Contact
from abc import ABC, abstractmethod

class ContactRepository(ABC):
    
    @abstractmethod
    def create_contact(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def get_contact_by_phonenumber(self, phonenumber: str) -> Contact:
        pass

    @abstractmethod
    def get_contacts_by_phonenumbers(self, phonenumbers: list[str]) -> list[Contact]:
        pass

    @abstractmethod
    def get_contact_by_email(self, email: str) -> Contact:
        pass

    @abstractmethod
    def get_contacts_by_emails(self, emails: list[str]) -> list[Contact]:
        pass

    @abstractmethod
    def update_contact(self, contact: Contact) -> Contact:
        pass
    
    @abstractmethod
    def delete_contact_by_phonenumber(self, phonenumber: str) -> None:
        pass

    @abstractmethod
    def delete_contact_by_email(self, email: str) -> None:
        pass