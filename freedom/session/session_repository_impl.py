import json

from redis import Redis
from freedom.session.session import Session
from freedom.session.session_repository import SessionRepository


class SessionRepositoryImpl(SessionRepository):
    
    SESSION_DIRECTORY: str = "chat:session"
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection
    
    def save(self, session: Session) -> None:
        self._redis_connection.set(
            f"{self.SESSION_DIRECTORY}:{session.session_id}",
            value=json.dumps(session.to_dict()))
    
    def get(self, session_id: str) -> Session:
        session_dict: dict =  json.loads(self._redis_connection.get(
            f"{self.SESSION_DIRECTORY}:{session_id}"))
        
        return Session.from_dict(session_dict)
    
    def update(self, session: Session) -> None:
        self.save(session)
    
    def delete(self, session_id: str) -> None:
        self._redis_connection.delete(
           f"{self.SESSION_DIRECTORY}:{session_id}")