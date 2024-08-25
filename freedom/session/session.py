import uuid
from enum import Enum
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from freedom.utils.serializable import Serializable


class SessionState(Enum):
    CREATED = 1
    WAITING = 2
    OPENED = 3
    INVALID = 4
    CLOSED = 5

@dataclass
class Session(Serializable):
    
    account_1_id: str
    account_2_id: str
    
    state: SessionState = field(default=SessionState.CREATED)

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    creation_timestamp: int = field(default_factory=lambda: int(datetime.now().timestamp()))
    max_timestamp: int = field(default_factory=lambda: int((datetime.now() + timedelta(days=1)).timestamp()))

    def is_valid(self) -> bool:
        return self.max_timestamp >= int(datetime.now().timestamp())
    
    def set_state(self, state: SessionState) -> None:
        self.state = state

    def to_dict(self) -> dict:
        return {
            "state": self.state.value,
            "account_1_id": self.account_1_id,
            "account_2_id": self.account_2_id,
            "session_id": self.session_id,
            "creation_timestamp": self.creation_timestamp,
            "max_timestamp": self.max_timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return Session(
            account_1_id=data.get("account_1_id"),
            account_2_id=data.get("account_2_id"),
            state=SessionState(data.get("state")),
            session_id=data.get("session_id"),
            creation_timestamp=data.get("creation_timestamp"),
            max_timestamp=data.get("max_timestamp")
        )