from dataclasses import dataclass, field
from datetime import datetime

from src.message.message import Message
from src.utils.serializable import Serializable

@dataclass
class Envelope(Serializable):
    
    messages: list[Message]
    timestamp: int = field(default_factory=lambda: int(datetime.now().timestamp()))

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "messages": [message.to_dict() for message in self.messages]
        }