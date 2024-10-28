import json

from freedomlib.crypto.functions import ED25519, X25519
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey, Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey, X25519PrivateKey


ED25519_KEYS_JSON: str = "./tests/resources/ed25519.json"
X25519_KEYS_JSON: str = "./tests/resources/x25519.json"

def test_load_ed25519_keys() -> None:
    with open(ED25519_KEYS_JSON) as f:
        keys: dict = json.loads(f.read())

    ed25519_public_key: Ed25519PublicKey = ED25519.load_public_key_from_pem(keys.get("ed25519_public_key"))
    ed25519_private_key: Ed25519PrivateKey = ED25519.load_private_key_from_pem(keys.get("ed25519_private_key"))
    
    assert isinstance(ed25519_public_key, Ed25519PublicKey)
    assert isinstance(ed25519_private_key, Ed25519PrivateKey)
    assert ED25519.public_key_to_pem(ed25519_private_key.public_key()).replace("\n", "") == keys.get("ed25519_public_key").replace("\n", "")

def test_load_x25519_keys() -> None:
    with open(X25519_KEYS_JSON) as f:
        keys: dict = json.loads(f.read())

    x25519_public_key: X25519PublicKey = X25519.load_public_key_from_pem(keys.get("x25519_public_key"))
    x25519_private_key: X25519PrivateKey = X25519.load_private_key_from_pem(keys.get("x25519_private_key"))
    
    assert isinstance(x25519_public_key, X25519PublicKey)
    assert isinstance(x25519_private_key, X25519PrivateKey)
    assert X25519.public_key_to_pem(x25519_private_key.public_key()).replace("\n", "") == keys.get("x25519_public_key").replace("\n", "")