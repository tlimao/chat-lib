from dataclasses import dataclass
from typing import Any

from freedomlib.utils.serializable import Serializable


@dataclass
class Key(Serializable):
    
    id: str
    aci: str
    pub_key: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "aci": self.aci,
            "pub_key": self.pub_key,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return Key(
            id=data.get("id"),
            aci=data.get("aci"),
            pub_key =data.get("pub_key")
        )