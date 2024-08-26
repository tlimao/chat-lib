import pytest

from freedomlib.crypto.account_keys import AccountKeys
from freedomlib.crypto.aes_gcm import AesGcm
from freedomlib.crypto.functions import EC25519

@pytest.fixture
def account_1_keys():
    return EC25519.create_key_pair()

@pytest.fixture
def account_2_keys():
    return EC25519.create_key_pair()

def test_key_exchange(account_1_keys: AccountKeys, account_2_keys: AccountKeys):
    shared_key_1: bytes = EC25519.shared_key(
        account_1_keys.private_key, account_2_keys.public_key)

    shared_key_2: bytes = EC25519.shared_key(
        account_2_keys.private_key, account_1_keys.public_key)

    derived_key_1: bytes = EC25519.derive_key(shared_key_1)
    derived_key_2: bytes = EC25519.derive_key(shared_key_2)
    
    assert derived_key_1 == derived_key_2
    
def test_encrypt_message(account_1_keys: AccountKeys, account_2_keys: AccountKeys):   
    shared_key_1: bytes = EC25519.shared_key(
        account_1_keys.private_key, account_2_keys.public_key)
    derived_key_1: bytes = EC25519.derive_key(shared_key_1)
    
    text: str = "This is a test"
    
    ciphertext, nonce, tag = AesGcm().encrypt(derived_key_1, text.encode("utf-8"))

    shared_key_2: bytes = EC25519.shared_key(
        account_2_keys.private_key, account_1_keys.public_key)
    derived_key_2: bytes = EC25519.derive_key(shared_key_2)
    
    decripted_text: str = AesGcm().decrypt(
        key=derived_key_2,
        ciphertext=ciphertext,
        nonce=nonce,
        tag=tag).decode("utf-8")
    
    assert decripted_text == text
    
    
    