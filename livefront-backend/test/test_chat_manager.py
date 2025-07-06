import pytest
from app.services.chat_manager import ChatManager

class DummyLLM:
    def generate(self, prompt):  # Should not be async unless your main code uses await
        return "Reply"
class DummyRAG:
    def retrieve(self, query, top_k=None): return []
class DummySession: pass

@pytest.mark.asyncio
async def test_chat_manager_handle(monkeypatch):
    mgr = ChatManager()
    mgr.llm = DummyLLM()
    mgr.rag = DummyRAG()

    # Patch get_user
    monkeypatch.setattr(
        "app.services.chat_manager.get_user",
        lambda session, uid: {"id": uid, "name": "Alice Smith", "school_name": "XYZ School"}
    )
    # Patch get_conversation_history
    monkeypatch.setattr(
        "app.services.chat_manager.get_conversation_history",
        lambda session, cid: []
    )

    # Patch add_message (async)
    calls = []
    async def fake_add_message(session, uid, cid, sender, msg):
        calls.append((uid, cid, sender, msg))
    monkeypatch.setattr("app.services.chat_manager.add_message", fake_add_message)

    # Run handle()
    conv_id, reply = await mgr.handle(DummySession(), 1, None, "Hello")

    # Assertions
    assert isinstance(conv_id, str)
    assert reply == "Reply"
    assert calls[0][2] == 'user'
    assert calls[1][2] == 'assistant'