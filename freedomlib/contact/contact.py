import json
from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass(frozen=True)
class Contact(Serializable):
    
    aci: str
    nick: str
    email: str
    phonenumber: str
    discoverable: bool
    x25519_pub_key: str
    ed25519_pub_key: str

    @staticmethod
    def from_json(json_data: str) -> 'Contact':
        return Contact(**json.loads(json_data))
    
    def to_dict(self) -> dict:
        return {
            "aci": self.aci,
            "nick": self.nick,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "discoverable": self.discoverable,
            "x25519_pub_key": self.x25519_pub_key,
            "ed25519_pub_key": self.ed25519_pub_key
        }

