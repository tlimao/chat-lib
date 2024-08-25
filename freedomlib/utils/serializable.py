from abc import ABC, abstractmethod
import base64
from typing import Any


class Serializable(ABC):
    
    @abstractmethod
    def to_dict(self) -> dict:
        ...

    @classmethod
    def bytes_to_str(cls, value: bytes) -> str:
        return base64.b64encode(value).decode('utf-8')

    @classmethod
    def str_to_bytes(cls, value: str) -> bytes:
        return base64.b64decode(value)