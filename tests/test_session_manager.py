import pytest
from fakeredis import FakeRedis
from unittest.mock import MagicMock
from freedomlib.session.error.session_not_found_error import SessionNotFoundError
from freedomlib.session.session_manager import SessionManager
from freedomlib.session.session import Session, SessionState
from freedomlib.session.error.session_not_created_error import SessionNotCreatedError
from freedomlib.session.session_repository import SessionRepository
from freedomlib.session.session_repository_impl import SessionRepositoryImpl

@pytest.fixture
def fake_redis():
    # Cria uma conexão fake do Redis usando fakeredis
    return FakeRedis()

@pytest.fixture
def mock_session_repository(fake_redis):
    # Passa a conexão fake do Redis para o SessionRepository
    return SessionRepositoryImpl(redis_connection=fake_redis)

@pytest.fixture
def session_manager(mock_session_repository):
    return SessionManager(mock_session_repository)

def test_create_session_success(session_manager: SessionManager):
    account_1_id: str = "account1"
    account_2_id: str = "account2"
        
    result: Session = session_manager.create_session(account_1_id, account_2_id)
    
    assert result.state == SessionState.CREATED
    assert result.account_1_id == account_1_id
    assert result.account_2_id == account_2_id

def test_create_session_failure(session_manager: SessionManager, mock_session_repository: SessionRepository):
    mock_session_repository.save = MagicMock(side_effect=Exception("Redis error"))
    
    with pytest.raises(SessionNotCreatedError) as excinfo:
        session_manager.create_session("account1", "account2")
    
    assert str(excinfo.value) == "Session not created: Redis error"

def test_get_session_success(session_manager: SessionManager, mock_session_repository: SessionRepository):
    session: Session = Session("account1", "account2")
    mock_session_repository.save(session)
    
    result: Session = session_manager.get_session(session.session_id)
    
    assert result.session_id == session.session_id

def test_get_session_failure(session_manager: SessionManager, mock_session_repository: SessionRepository):
    mock_session_repository.get = MagicMock(side_effect=Exception("Session not found"))
    
    with pytest.raises(SessionNotFoundError) as excinfo:
        session_manager.get_session("invalid_account_id")
    
    assert str(excinfo.value) == "Session not found: Session not found"
