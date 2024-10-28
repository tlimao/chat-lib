from dataclasses import dataclass, field
from datetime import datetime

from freedomlib.utils.serializable import Serializable


@dataclass(frozen=True)
class Message(Serializable):

    id: str
    sender_aci: str
    recipient_aci: str
    nonce: bytes
    tag: bytes
    cipher_message: bytes
    timestamp: int = field(default_factory=lambda: int(datetime.now().timestamp()))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sender_aci": self.sender_aci,
            "recipient_aci": self.recipient_aci,
            "nonce": Serializable.bytes_to_b64_str(self.nonce),
            "tag": Serializable.bytes_to_b64_str(self.tag),
            "cipher_message": Serializable.bytes_to_b64_str(self.cipher_message),
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        return Message(
            id=data.get("id"),
            sender_aci=data.get("sender_aci"),
            recipient_aci=data.get("recipient_aci"),
            nonce=Serializable.b64_str_to_bytes(data.get("nonce")),
            tag=Serializable.b64_str_to_bytes(data.get("tag")),
            cipher_message=Serializable.b64_str_to_bytes(data.get("cipher_message")),
            timestamp=data.get("timestamp")
        )