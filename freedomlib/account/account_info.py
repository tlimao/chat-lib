from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable


@dataclass(frozen=True)
class AccountInfo(Serializable):

    nick: str
    email: str

    def to_dict(self) -> dict:
        return {
            "nick": self.nick,
            "email": self.email
        }
    
    