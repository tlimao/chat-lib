from abc import ABC, abstractmethod

from freedom.session.session import Session


class SessionRepository(ABC):
    
    @abstractmethod
    def save(self, session: Session) -> None:
        ...

    @abstractmethod
    def get(self, session_id: str) -> Session:
        ...

    @abstractmethod
    def update(self, session: Session) -> None:
        ...

    @abstractmethod
    def delete(self, session_id: str) -> None:
        ...