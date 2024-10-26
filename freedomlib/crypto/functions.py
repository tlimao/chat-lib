from abc import ABC
from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

class X25519(ABC):
    
    @classmethod
    def create_key_pair(cls) -> Tuple:
        private_key: X25519PrivateKey = X25519PrivateKey.generate()
        public_key: X25519PublicKey = private_key.public_key()
        
        return (private_key, public_key)

    @classmethod
    def derive_key(cls, shared_key: bytes, length: int = 32, salt: bytes = b'', info: bytes = b'') -> bytes:
        return HKDF(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            info=info).derive(shared_key)

    @classmethod
    def shared_key(cls, private_key: X25519PrivateKey, public_key: X25519PublicKey) -> bytes:
        return private_key.exchange(public_key)
    
    @classmethod
    def load_public_key_from_pem(cls) -> X25519PublicKey:
        ...

    @classmethod
    def load_private_key_from_pem(cls) -> X25519PrivateKey:
        ...

class ED25519(ABC):
    
    @classmethod
    def create_key_pair(cls) -> Tuple:
        private_key: Ed25519PrivateKey = Ed25519PrivateKey.generate()
        public_key: Ed25519PublicKey = private_key.public_key()
        
        return (private_key, public_key)
    
    @classmethod
    def sign(cls, private_key: Ed25519PrivateKey, data: bytes) -> bytes:
        return private_key.sign(data)

    @classmethod
    def verify(cls, public_key: Ed25519PublicKey, signature: bytes,  data: bytes) -> None:
        return public_key.verify(signature, data)

    @classmethod
    def load_public_key_from_pem(cls) -> Ed25519PublicKey:
        ...

    @classmethod
    def load_private_key_from_pem(cls) -> Ed25519PrivateKey:
        ...
        