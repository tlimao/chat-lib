import json
from freedomlib.contact.contact_repository import ContactRepository
from freedomlib.contact.contact import Contact
from freedomlib.contact.error.contact_not_found_error import ContactNotFoundError
from redis import Redis

class ContactRepositoryImpl(ContactRepository):
    
    CONTACT_KEY_PREFIX = "chat:contact"
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection

    def create_contact(self, contact: Contact) -> Contact:
        contact_data = json.dumps(contact.to_dict())
        self._redis_connection.set(f"{self.CONTACT_KEY_PREFIX}:phonenumber:{contact.phonenumber}", contact_data)
        self._redis_connection.set(f"{self.CONTACT_KEY_PREFIX}:email:{contact.email}", contact_data)
        return contact
    
    def get_contact_by_phonenumber(self, phonenumber: str) -> Contact:
        contact_data = self._redis_connection.get(f"{self.CONTACT_KEY_PREFIX}:phonenumber:{phonenumber}")
        if contact_data:
            return Contact.from_json(contact_data)
        else:
            raise ContactNotFoundError(f"Contact with phone number {phonenumber} not found")
    
    def get_contacts_by_phonenumbers(self, phonenumbers: list[str]) -> list[Contact]:
        contact_data = self._redis_connection.mget([f"{self.CONTACT_KEY_PREFIX}:phonenumber:{phonenumber}" for phonenumber in phonenumbers])
        return [Contact.from_json(contact) for contact in contact_data]

    def get_contact_by_email(self, email: str) -> Contact:
        contact_data = self._redis_connection.get(f"{self.CONTACT_KEY_PREFIX}:email:{email}")
        if contact_data:
            return Contact.from_json(contact_data)
        else:
            raise ContactNotFoundError(f"Contact with email {email} not found")

    def get_contacts_by_emails(self, emails: list[str]) -> list[Contact]:
        contact_data = self._redis_connection.mget([f"{self.CONTACT_KEY_PREFIX}:email:{email}" for email in emails])
        return [Contact.from_json(contact) for contact in contact_data]

    def update_contact(self, contact: Contact) -> Contact:
        return self.create_contact(contact)

    def delete_contact_by_phonenumber(self, phonenumber: str) -> None:
        contact = self.get_contact_by_phonenumber(phonenumber)
        self._redis_connection.delete(f"{self.CONTACT_KEY_PREFIX}:phonenumber:{contact.phonenumber}")
        self._redis_connection.delete(f"{self.CONTACT_KEY_PREFIX}:email:{contact.email}")

    def delete_contact_by_email(self, email: str) -> None:
        contact = self.get_contact_by_email(email)
        self._redis_connection.delete(f"{self.CONTACT_KEY_PREFIX}:phonenumber:{contact.phonenumber}")
        self._redis_connection.delete(f"{self.CONTACT_KEY_PREFIX}:email:{contact.email}")