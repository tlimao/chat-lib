from dataclasses import dataclass
from typing import Any

from src.utils.serializable import Serializable


@dataclass(frozen=True)
class Account(Serializable):
    
    id: str
    nick: str
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nick": self.nick
        }

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return Account(
            id=data.get("id"),
            nick=data.get("nick")
        )