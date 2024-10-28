from abc import ABC, abstractmethod
import base64
from typing import Any


class Serializable(ABC):
    
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def bytes_to_str(cls, value: bytes, encoding: str = 'utf-8') -> str:
        return value.decode(encoding)

    @classmethod
    def bytes_to_b64_str(cls, value: bytes, encoding: str = 'utf-8') -> str:
        return base64.b64encode(value).decode(encoding)

    @classmethod
    def str_to_bytes(cls, value: str, encoding: str = 'utf-8') -> bytes:
        return value.encode(encoding)

    @classmethod
    def b64_str_to_bytes(cls, value: str, encoding: str = 'utf-8') -> bytes:
        return base64.b64decode(value)