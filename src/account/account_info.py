from dataclasses import dataclass

from src.utils.serializable import Serializable


@dataclass(frozen=True)
class AccountInfo(Serializable):
    
    id: str
    nick: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nick": self.nick
        }
    
    