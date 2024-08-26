from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import NoEncryption, BestAvailableEncryption

@dataclass
class AccountKeys:
    
    private_key: X25519PrivateKey
    public_key: X25519PublicKey
    
    def get_public_key_pem(self) -> str:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def get_private_key_pem(self, password: str = None) -> str:
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=BestAvailableEncryption(password) if (password) else NoEncryption())