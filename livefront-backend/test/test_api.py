import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app, chat_mgr
from app.config import settings

# ----- Fixtures -----
@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

# ----- API Endpoint Tests -----

def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert all(isinstance(u.get("id"), int) and isinstance(u.get("name"), str) for u in users)

@ pytest.mark.parametrize("user_id", [1, 2])
def test_get_welcome(client, user_id):
    response = client.get(f"/welcome/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert isinstance(data["messages"], list)
    # Each welcome message should be a string
    assert all(isinstance(msg, str) for msg in data["messages"])

@pytest.mark.asyncio
async def test_chat_endpoint_returns_reply(async_client, monkeypatch):
    # Stub LLMService.generate to return a predictable reply
    async def fake_generate(prompt: str) -> str:
        return "Hello from test!"
    monkeypatch.setattr(chat_mgr.llm, "generate", fake_generate)
    # Stub RAGService.retrieve to return no hits
    monkeypatch.setattr(chat_mgr.rag, "retrieve", lambda query, top_k=None: [])

    payload = {"user_id": 1, "message": "Hello"}
    response = await async_client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert isinstance(data["conversation_id"], str)
    assert data.get("reply") == "Hello from test!"

@pytest.mark.asyncio
async def test_chat_endpoint_persistence(async_client, monkeypatch):
    # Stub LLMService.generate
    async def fake_generate(prompt: str) -> str:
        return "Persistent reply"
    monkeypatch.setattr(chat_mgr.llm, "generate", fake_generate)
    # Ensure no RAG hits
    monkeypatch.setattr(chat_mgr.rag, "retrieve", lambda query, top_k=None: [])

    # First message
    payload = {"user_id": 1, "message": "First"}
    resp1 = await async_client.post("/chat", json=payload)
    cid = resp1.json().get("conversation_id")
    assert cid

    # Second message using same conversation_id
    payload2 = {"user_id": 1, "conversation_id": cid, "message": "Second"}
    resp2 = await async_client.post("/chat", json=payload2)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2.get("conversation_id") == cid
    assert data2.get("reply") == "Persistent reply"
