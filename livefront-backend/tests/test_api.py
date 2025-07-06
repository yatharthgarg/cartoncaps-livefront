import pytest

import app.main as main_mod
import app.api.users as users_mod
import app.api.chat as chat_mod

class TestHealthAndWelcome:
    def test_health(self, client):
        """
        The /health endpoint should return {"status":"ok"}
        """
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_welcome_user_not_found(self, client, monkeypatch):
        """
        If get_user returns None, /welcome/{id} should 404
        """
        async def fake_get_user(session, user_id):
            return None
        monkeypatch.setattr(main_mod, "get_user", fake_get_user)

        resp = client.get("/welcome/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "User not found"

    def test_welcome_success(self, client, monkeypatch):
        """
        Successful welcome returns personalized messages
        """
        user_data = {"name": "Alice Liddell", "school_name": "Wonder Academy"}
        async def fake_get_user(session, user_id):
            return user_data
        monkeypatch.setattr(main_mod, "get_user", fake_get_user)

        resp = client.get("/welcome/1")
        assert resp.status_code == 200
        messages = resp.json()["messages"]
        greeting, prompt = messages
        assert greeting.startswith(f"Hi {user_data['name']}!")
        assert "Wonder Academy" in greeting
        assert "Ask me a question" in prompt

class TestUsersEndpoint:
    def test_list_users(self, client, monkeypatch):
        """
        GET /users should return all users
        """
        fake_users = [{"id":1,"name":"Anna"},{"id":2,"name":"Bob"}]
        async def fake_get_all_users(session):
            return fake_users
        monkeypatch.setattr(users_mod, "get_all_users", fake_get_all_users)

        resp = client.get("/users")
        assert resp.status_code == 200
        assert resp.json() == fake_users

class TestChatEndpoint:
    def test_chat_success(self, client, monkeypatch):
        """
        POST /chat returns stubbed reply
        """
        async def fake_init(session):
            pass
        async def fake_handle(session, user_id, conv_id, message):
            return ("conv-1234", "Hello from test!")
        monkeypatch.setattr(chat_mod.chat_mgr, "initialize", fake_init)
        monkeypatch.setattr(chat_mod.chat_mgr, "handle", fake_handle)

        payload = {"user_id":1,"conversation_id":None,"message":"Hi there!"}
        resp = client.post("/chat", json=payload)
        assert resp.status_code == 200
        assert resp.json() == {"conversation_id":"conv-1234","reply":"Hello from test!"}

    def test_chat_server_error(self, client, monkeypatch):
        """
        POST /chat raises server error when handle fails
        """
        async def fake_init(session):
            pass
        async def fake_handle(session, user_id, conv_id, message):
            raise RuntimeError("oh no")
        monkeypatch.setattr(chat_mod.chat_mgr, "initialize", fake_init)
        monkeypatch.setattr(chat_mod.chat_mgr, "handle", fake_handle)

        payload = {"user_id":1,"conversation_id":None,"message":"Hi error"}
        resp = client.post("/chat", json=payload)
        assert resp.status_code == 500
        assert "RuntimeError: oh no" in resp.json()["detail"]