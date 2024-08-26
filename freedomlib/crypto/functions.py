import os
from abc import ABC, abstractmethod
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey

from freedomlib.crypto.account_keys import AccountKeys

class EC25519(ABC):
    
    @classmethod
    def create_key_pair(cls) -> AccountKeys:
        private_key: X25519PrivateKey = X25519PrivateKey.generate()
        public_key: X25519PublicKey = private_key.public_key()
        
        return AccountKeys(private_key=private_key, public_key=public_key)

    @classmethod
    def derive_key(cls, shared_key: bytes) -> bytes:
        return HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data').derive(shared_key)

    @classmethod
    def shared_key(cls, private_key: X25519PrivateKey, public_key: X25519PublicKey) -> bytes:
        return private_key.exchange(public_key)