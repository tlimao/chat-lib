from abc import ABC
from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

class X25519(ABC):
    
    @classmethod
    def create_key_pair(cls) -> Tuple:
        """ Return a tuple (x25519 private key, x25519 public key) """
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
    def private_key_to_pem(cls, private_key: Ed25519PrivateKey, password: str = None) -> str:
        encryption_algorithm: serialization.KeySerializationEncryption = serialization.NoEncryption()
        
        if password:
            encryption_algorithm: serialization.KeySerializationEncryption = serialization.BestAvailableEncryption(password.encode("utf-8"))
        
        return private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption_algorithm
            ).decode('utf-8')
    
    @classmethod
    def public_key_to_pem(cls, public_key: X25519PublicKey) -> str:
        return public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

    @classmethod
    def load_public_key_from_pem(cls, public_key_pem: str) -> X25519PublicKey:
        return serialization.load_pem_public_key(public_key_pem.encode("utf-8"))

    @classmethod
    def load_private_key_from_pem(cls, private_key_pem: str, password: str = None) -> X25519PrivateKey:
        return serialization.load_pem_private_key(
                private_key_pem.encode("utf-8"), 
                password=password.encode("utf-8") if password else None
            ) 

class ED25519(ABC):
    
    @classmethod
    def create_key_pair(cls) -> Tuple:
        """ Return a tuple (ed25519 private key, ed25519 public key) """
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
    def private_key_to_pem(cls, private_key: Ed25519PrivateKey, password: str = None) -> str:
        encryption_algorithm: serialization.KeySerializationEncryption = serialization.NoEncryption()
        
        if password:
            encryption_algorithm: serialization.KeySerializationEncryption = serialization.BestAvailableEncryption(password.encode("utf-8"))
        
        return private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption_algorithm
            ).decode('utf-8')
        
    @classmethod
    def public_key_to_pem(cls, public_key: X25519PublicKey) -> str:
        return public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

    @classmethod
    def load_public_key_from_pem(cls, public_key_pem: str) -> Ed25519PublicKey:
        return serialization.load_pem_public_key(public_key_pem.encode("utf-8"))

    @classmethod
    def load_private_key_from_pem(cls, private_key_pem: str, password: str = None) -> Ed25519PrivateKey:
        return serialization.load_pem_private_key(
                private_key_pem.encode("utf-8"),
                password=password.encode("utf-8") if password else None
            )
    