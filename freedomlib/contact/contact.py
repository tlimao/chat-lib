import json
from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass(frozen=True)
class Contact(Serializable):
    
    id: str
    nick: str
    email: str
    phonenumber: str

    @staticmethod
    def from_json(json_data: str) -> 'Contact':
        return Contact(**json.loads(json_data))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nick": self.nick,
            "email": self.email,
            "phonenumber": self.phonenumber
        }

