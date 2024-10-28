import json

from freedomlib.account.account import Account

ACCOUNT_JSON_FILE: str = './tests/resources/account.json'

def test_load_account_from_json() -> None:
    with open(ACCOUNT_JSON_FILE, 'r', encoding='utf-8') as f:
        account_data: dict = json.load(f)
        
    account: Account = Account.from_dict(account_data)
    
    assert account.aci == account_data.get("aci")
    assert account.nick == account_data.get("nick")
    assert account.email == account_data.get("email")
    assert account.phonenumber == account_data.get("phonenumber")
    assert account.discoverable == account_data.get("discoverable")
    assert account.pin_hash == account_data.get("pin_hash")
    
    account_dict: dict = account.to_dict()
    
    assert account_dict.get("aci") == account_data.get("aci")
    assert account_dict.get("nick") == account_data.get("nick")
    assert account_dict.get("email") == account_data.get("email")
    assert account_dict.get("phonenumber") == account_data.get("phonenumber")
    assert account_dict.get("discoverable") == account_data.get("discoverable")
    assert account_dict.get("pin_hash") == account_data.get("pin_hash")