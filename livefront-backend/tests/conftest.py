import pytest
from fastapi.testclient import TestClient
from app.main import app as fastapi_app

import app.api.users as users_mod
import app.api.chat as chat_mod

class DummySession:
    """A dummy session object; methods on it can be stubbed as needed."""
    pass

class DummyAsyncCM:
    """An async context manager that yields a DummySession."""
    def __init__(self):
        self.session = DummySession()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

def dummy_session_factory():
    """Factory to replace AsyncSessionLocal everywhere."""
    return DummyAsyncCM()

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    monkeypatch.setattr("app.main.AsyncSessionLocal", dummy_session_factory)
    monkeypatch.setattr(users_mod, "AsyncSessionLocal", dummy_session_factory)
    monkeypatch.setattr(chat_mod, "AsyncSessionLocal", dummy_session_factory)

@pytest.fixture
def client():
    """Return a TestClient against the FastAPI app."""
    return TestClient(fastapi_app)