from abc import ABC, abstractmethod

from freedomlib.session.session_key import SessionKey


class SessionKeyRepository(ABC):

    @abstractmethod
    def get(self, key_id: str) -> SessionKey:
        raise NotImplementedError()

    @abstractmethod
    def get_key_by_aci(self, aci: str) -> SessionKey:
        raise NotImplementedError()
    
    @abstractmethod
    def save(self, session_key: SessionKey) -> SessionKey:
        raise NotImplementedError()

    @abstractmethod
    def update(self, session_key: SessionKey) -> SessionKey:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, key_id: str) -> None:
        raise NotImplementedError()