import json
from dataclasses import dataclass

@dataclass
class AccountInfoCreated:
    
    account_id: str
    device_id: int
    nick: str
    email: str
    phonenumber: str
    public_key: str
    
    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "nick": self.nick,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "public_key": self.public_key,
            "device_id": self.device_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AccountInfoCreated":
        return cls(
            account_id=data["account_id"],
            device_id=data["device_id"],
            nick=data["nick"],
            email=data["email"],
            phonenumber=data["phonenumber"],
            public_key=data["public_key"]
        )
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())