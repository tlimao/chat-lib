from freedomlib.contact.contact_repository import ContactRepository
from freedomlib.contact.contact import Contact
from freedomlib.contact.error.contact_not_found_error import ContactNotFoundError
from freedomlib.contact.error.contact_not_created_error import ContactNotCreatedError
from freedomlib.contact.error.contact_not_updated_error import ContactNotUpdatedError
from freedomlib.contact.error.contact_not_deleted_error import ContactNotDeletedError

class ContactManager:

    def __init__(self, contact_repository: ContactRepository) -> None:
        self._contact_repository: ContactRepository = contact_repository

    def create_contact(self, contact: Contact) -> Contact:
        try:
            return self._contact_repository.create_contact(contact)
        except Exception as e:
            raise ContactNotCreatedError(f"Contact not created: {e}")

    def get_contact_by_phonenumber(self, phonenumber: str) -> Contact:
        try:
            return self._contact_repository.get_contact_by_phonenumber(phonenumber)
        except Exception as e:
            raise ContactNotFoundError(f"Contact not found: {e}")

    def get_contacts_by_phonenumbers(self, phonenumbers: list[str]) -> list[Contact]:
        try:
            return self._contact_repository.get_contacts_by_phonenumbers(phonenumbers)
        except Exception as e:
            raise ContactNotFoundError(f"Contact not found: {e}")

    def get_contact_by_email(self, email: str) -> Contact:
        try:
            return self._contact_repository.get_contact_by_email(email)
        except Exception as e:
            raise ContactNotFoundError(f"Contact not found: {e}")

    def get_contacts_by_emails(self, emails: list[str]) -> list[Contact]:
        try:
            return self._contact_repository.get_contacts_by_emails(emails)
        except Exception as e:
            raise ContactNotFoundError(f"Contact not found: {e}")

    def update_contact(self, contact: Contact) -> Contact:
        try:
            return self._contact_repository.update_contact(contact)
        except Exception as e:
            raise ContactNotUpdatedError(f"Contact not updated: {e}")

    def delete_contact_by_phonenumber(self, phonenumber: str) -> None:
        try:
            return self._contact_repository.delete_contact_by_phonenumber(phonenumber)
        except Exception as e:
            raise ContactNotDeletedError(f"Contact not deleted: {e}")

    def delete_contact_by_email(self, email: str) -> None:
        try:
            return self._contact_repository.delete_contact_by_email(email)
        except Exception as e:
            raise ContactNotDeletedError(f"Contact not deleted: {e}")