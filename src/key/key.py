from dataclasses import dataclass
from typing import Any

from src.utils.serializable import Serializable


@dataclass
class Key(Serializable):
    
    id: str
    account_id: str
    pub_key: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "pub_key": self.pub_key,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return Key(
            id=data.get("id"),
            account_id=data.get("account_id"),
            pub_key =data.get("pub_key")
        )