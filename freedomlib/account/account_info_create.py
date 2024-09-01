import json
from dataclasses import dataclass

@dataclass
class AccountInfoCreate:
    nick: str
    email: str
    phonenumber: str
    public_key: str
    
    def to_dict(self) -> dict:
        return {
            "nick": self.nick,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "public_key": self.public_key
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: dict) -> "AccountInfoCreate":
        return cls(
            nick=data["nick"],
            email=data["email"],
            phonenumber=data["phonenumber"],
            public_key=data["public_key"]
        )