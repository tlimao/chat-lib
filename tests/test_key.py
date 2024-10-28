import os
import json

from freedomlib.crypto.functions import ED25519, X25519
from freedomlib.key.key_box import KeyBox
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes, base

from freedomlib.utils.serializable import Serializable

KEY_BOX_JSON_FILE: str = "./tests/resources/key_box.json"

RICKY_MESSAGE: str = "Hi Morty! Come with me!"
MORTY_MESSAGE: str = "Oohhh Ricky!!! Noooo!!"

def test_load_key_from_json() -> None:
    with open(KEY_BOX_JSON_FILE, 'r', encoding='utf-8') as f:
        key_box_data: dict = json.load(f)

    key_box: KeyBox = KeyBox.from_dict(key_box_data)
    
    assert key_box.id == key_box_data.get("id")
    assert key_box.aci == key_box_data.get("aci")
    assert key_box.ed25519_public_key == key_box_data.get("ed25519_public_key")
    assert key_box.x25519_public_key == key_box_data.get("x25519_public_key")
    
    key_box_json: dict = key_box.to_dict()
    
    assert key_box_json.get("id") == key_box_data.get("id")
    assert key_box_json.get("aci") == key_box_data.get("aci")
    assert key_box_json.get("ed25519_public_key") == key_box_data.get("ed25519_public_key")
    assert key_box_json.get("x25519_public_key") == key_box_data.get("x25519_public_key")
    
    assert isinstance(key_box.load_signing_key(), Ed25519PublicKey)
    assert isinstance(key_box.load_exchange_key(), X25519PublicKey)

def test_key_exchange() -> None:
    # Ricky keys
    ricky_x25519_private_key, ricky_x25519_public_key = X25519.create_key_pair()

    # Morty keys
    morty_x25519_private_key, morty_x25519_public_key = X25519.create_key_pair()
    
    message: str = "Hi Morty! Come with me!"
    
    ricky_shared_key = X25519.shared_key(ricky_x25519_private_key, morty_x25519_public_key)
    ricky_derived_key = X25519.derive_key(ricky_shared_key)
    
    nonce: bytes = os.urandom(12)

    encryptor: base.AEADEncryptionContext = Cipher(
        algorithms.AES(ricky_derived_key),
        modes.GCM(nonce)).encryptor()
    
    chiper_message: bytes = encryptor.update(Serializable.str_to_bytes(message)) + encryptor.finalize()
    
    tag: bytes = encryptor.tag
    
    morty_shared_key = X25519.shared_key(morty_x25519_private_key, ricky_x25519_public_key)
    morty_derived_key = X25519.derive_key(morty_shared_key)
    
    decryptor: base.AEADEncryptionContext = Cipher(
        algorithms.AES(morty_derived_key),
        modes.GCM(nonce, tag)).decryptor()
    
    original_message: str = Serializable.bytes_to_str(
        decryptor.update(chiper_message) + decryptor.finalize()
    )
    
    assert message == original_message
    
def test_signing_keys() -> None:
    # Ricky keys
    ricky_ed25519_private_key, ricky_ed25519_public_key = ED25519.create_key_pair()

    # Morty keys
    morty_ed25519_private_key, morty_ed25519_public_key = ED25519.create_key_pair()
    
    ricky_message: str = RICKY_MESSAGE
    
    ricky_signature: str = Serializable.bytes_to_b64_str(
        ED25519.sign(ricky_ed25519_private_key, Serializable.str_to_bytes(ricky_message))
    )
    
    # Morty Conference
    assert ED25519.verify(ricky_ed25519_public_key, Serializable.b64_str_to_bytes(ricky_signature), Serializable.str_to_bytes(ricky_message)) == None
    
    morty_message: str = MORTY_MESSAGE
    
    morty_signature: str = Serializable.bytes_to_b64_str(
        ED25519.sign(morty_ed25519_private_key, Serializable.str_to_bytes(morty_message))
    )
    
    # Ricky Conference
    assert ED25519.verify(morty_ed25519_public_key, Serializable.b64_str_to_bytes(morty_signature), Serializable.str_to_bytes(morty_message)) == None
    
    
    
    
    