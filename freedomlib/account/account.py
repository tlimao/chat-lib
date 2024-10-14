from dataclasses import dataclass
from typing import Any

from freedomlib.utils.serializable import Serializable


@dataclass(frozen=True)
class Account(Serializable):
    
    aci: str
    nick: str
    email: str
    phonenumber: str
    discoverable: bool
    pin_hash: str

    def to_dict(self) -> dict:
        return {
            "aci": self.aci,
            "nick": self.nick,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "discoverable": self.discoverable,
            "pin_hash": self.pin_hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return Account(
            aci=data.get("aci"),
            nick=data.get("nick"),
            email=data.get("email"),
            phonenumber=data.get("phonenumber"),
            discoverable=data.get("discoverable"),
            pin_hash=data.get("pin_hash")
        )