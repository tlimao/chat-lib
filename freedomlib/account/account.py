from dataclasses import dataclass
from typing import Any

from freedomlib.utils.serializable import Serializable


@dataclass(frozen=True)
class Account(Serializable):
    
    id: str
    nick: str
    email: str
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nick": self.nick,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return Account(
            id=data.get("id"),
            nick=data.get("nick"),
            email=data.get("email")
        )