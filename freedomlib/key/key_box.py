from dataclasses import dataclass
from freedomlib.utils.serializable import Serializable
from freedomlib.crypto.functions import ED25519, X25519
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey

@dataclass
class KeyBox(Serializable):
    
    id: str
    aci: str
    ed25519_public_key: str
    x25519_public_key: str

    def to_dict(self) -> dict:
        return self.__dict__

    def load_signing_key(self) -> Ed25519PublicKey:
        return ED25519.load_public_key_from_pem(self.ed25519_public_key)

    def load_exchange_key(self) -> X25519PublicKey:
        return X25519.load_public_key_from_pem(self.x25519_public_key)

    @classmethod
    def from_dict(cls, data: dict) -> 'KeyBox':
        return KeyBox(**data)