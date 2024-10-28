from dataclasses import dataclass

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
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> 'Account':
        return Account(**data)