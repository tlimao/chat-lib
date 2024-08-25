from src.session.error.session_not_found_error import SessionNotFoundError
from src.session.error.session_not_created_error import SessionNotCreatedError
from src.session.session_repository import SessionRepository
from src.session.session import Session


class SessionManager:
    
    def __init__(self, session_repository: SessionRepository) -> None:
        self._session_repository: SessionRepository = session_repository

    def create_session(self, account_1_id: str, account_2_id: str) -> None:
        try:
            session: Session = Session(account_1_id=account_1_id, account_2_id=account_2_id)
            
            self._session_repository.save(session)
            
            return session
        except Exception as e:
            raise SessionNotCreatedError(f"Session not created: {e}")      
    
    def get_session(self, session_id: str) -> Session:
        try:
            return self._session_repository.get(session_id)
        except Exception as e:
            raise SessionNotFoundError(f"Session not found: {e}")
        