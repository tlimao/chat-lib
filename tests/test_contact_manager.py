import pytest
from fakeredis import FakeRedis
from unittest.mock import MagicMock

from freedomlib.contact.contact_manager import ContactManager
from freedomlib.contact.contact_repository import ContactRepository
from freedomlib.contact.contact_repository_impl import ContactRepositoryImpl
from freedomlib.contact.contact import Contact
from freedomlib.contact.error.contact_not_found_error import ContactNotFoundError

@pytest.fixture
def fake_redis():
    # Cria uma conexão fake do Redis usando fakeredis
    return FakeRedis()

@pytest.fixture
def mock_contact_repository(fake_redis):
    # Passa a conexão fake do Redis para o SessionRepository
    return ContactRepositoryImpl(redis_connection=fake_redis)

@pytest.fixture
def contact_manager(mock_contact_repository):
    return ContactManager(mock_contact_repository)

def test_create_contact(contact_manager: ContactManager):
    contact: Contact = Contact(
        id="1",
        nick="John Doe",
        email="john.doe@example.com",
        phonenumber="1234567890",
        pub_key="------BEGIN KEY ------- ....."
    )
    contact = contact_manager.create_contact(contact)
    assert contact.id == "1"
    assert contact.nick == "John Doe"

def test_get_contact(contact_manager: ContactManager):
    contact: Contact = Contact(
        id="1",
        nick="John Doe",
        email="john.doe@example.com",
        phonenumber="1234567890",
        pub_key="------BEGIN KEY ------- ....."
    )
    contact = contact_manager.create_contact(contact)
    contact = contact_manager.get_contact_by_phonenumber("1234567890")
    assert contact.id == "1"
    assert contact.nick == "John Doe"

def test_update_contact(contact_manager: ContactManager):
    contact: Contact = Contact(
        id="1",
        nick="John Doe",
        email="john.doe@example.com",
        phonenumber="1234567890",
        pub_key="------BEGIN KEY ------- ....."
    )
    contact = contact_manager.update_contact(contact)
    assert contact.id == "1"
    assert contact.nick == "John Doe"

def test_delete_contact_by_phonenumber(contact_manager: ContactManager):
    contact: Contact = Contact(
        id="1",
        nick="John Doe",
        email="john.doe@example.com",
        phonenumber="1234567890",
        pub_key="------BEGIN KEY ------- ....."
    )
    contact = contact_manager.create_contact(contact)
    contact_manager.delete_contact_by_phonenumber("1234567890")
    with pytest.raises(ContactNotFoundError):
        contact_manager.get_contact_by_phonenumber("1234567890")

def test_delete_contact_by_email(contact_manager: ContactManager):
    contact: Contact = Contact(
        id="1",
        nick="John Doe",
        email="john.doe@example.com",
        phonenumber="1234567890",
        pub_key="------BEGIN KEY ------- ....."
    )
    contact = contact_manager.create_contact(contact)
    contact_manager.delete_contact_by_email("john.doe@example.com")
    with pytest.raises(ContactNotFoundError):
        contact_manager.get_contact_by_email("john.doe@example.com")