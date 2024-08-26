from dataclasses import dataclass


@dataclass(frozen=True)
class KeyInfo:
    
    account_id: str
    pub_key: str
    
    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "pub_key": self.pub_key
        }