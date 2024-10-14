import json
from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass(frozen=True)
class Contact(Serializable):
    
    aci: str
    nick: str
    email: str
    phonenumber: str
    pub_key: str

    @staticmethod
    def from_json(json_data: str) -> 'Contact':
        return Contact(**json.loads(json_data))
    
    def to_dict(self) -> dict:
        return {
            "aci": self.aci,
            "nick": self.nick,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "pub_key": self.pub_key
        }

