import json

from freedomlib.contact.contact import Contact

CONTACT_JSON_FILE: str = './tests/resources/contact.json'

def test_load_contact_from_json() -> None:
    with open(CONTACT_JSON_FILE, 'r', encoding='utf-8') as f:
        contact_data: dict = json.load(f)
        
    contact: Contact = Contact.from_dict(contact_data)
    
    assert contact.aci == contact_data.get("aci")
    assert contact.nick == contact_data.get("nick")
    assert contact.email == contact_data.get("email")
    assert contact.phonenumber == contact_data.get("phonenumber")
    
    contact_dict: dict = contact.to_dict()
    
    assert contact_dict.get("aci") == contact_data.get("aci")
    assert contact_dict.get("nick") == contact_data.get("nick")
    assert contact_dict.get("email") == contact_data.get("email")
    assert contact_dict.get("phonenumber") == contact_data.get("phonenumber")