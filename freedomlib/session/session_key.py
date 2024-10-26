from dataclasses import dataclass
from typing import Any

from freedomlib.utils.serializable import Serializable


@dataclass
class SessionKey(Serializable):
    
    id: str
    aci: str
    x25519_pub_key: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "aci": self.aci,
            "x25519_pub_key": self.x25519_pub_key
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SessionKey':
        return SessionKey(
            id=data.get("id"),
            aci=data.get("aci"),
            x25519_pub_key=data.get("x25519_pub_key")
        )