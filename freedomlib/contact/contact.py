from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass(frozen=True)
class Contact(Serializable):
    
    aci: str
    nick: str
    email: str
    phonenumber: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Contact':
        return Contact(**data)
    
    def to_dict(self) -> dict:
        return self.__dict__

