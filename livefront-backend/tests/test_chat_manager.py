import pytest
import uuid
from unittest.mock import AsyncMock

import app.services.chat_manager as cm_mod
from app.services.chat_manager import ChatManager
from app.config import settings

@pytest.fixture(autouse=True)
def patch_settings(monkeypatch):
    monkeypatch.setattr(settings, "DEFAULT_RECOMMEND_K", 1)
    monkeypatch.setattr(settings, "MORE_K", 1)
    monkeypatch.setattr(settings, "RAG_TOP_K", 5)
    monkeypatch.setattr(settings, "MAX_HISTORY", 5)

@pytest.mark.asyncio
async def test_initialize_builds_index():
    mgr = ChatManager()
    mgr.rag.build_index = AsyncMock()
    await mgr.initialize("dummy_session")
    mgr.rag.build_index.assert_awaited_once_with("dummy_session")

@pytest.mark.asyncio
async def test_handle_unknown_user(monkeypatch):
    mgr = ChatManager()
    monkeypatch.setattr(cm_mod, "get_user", AsyncMock(return_value=None))
    with pytest.raises(ValueError):
        await mgr.handle("dummy_session", user_id=42, conversation_id=None, message="hello")

@pytest.mark.asyncio
async def test_default_flow(monkeypatch):
    mgr = ChatManager()
    monkeypatch.setattr(cm_mod, "get_user", AsyncMock(return_value={"name": "Bob", "school_name": None}))
    monkeypatch.setattr(cm_mod, "get_conversation_history", AsyncMock(return_value=[]))
    monkeypatch.setattr(cm_mod, "add_message", AsyncMock())

    class DummyRag:
        def match_faq(self, message):
            return None
        def match_rule(self, message):
            return None
        def retrieve(self, query, top_k=None):
            return [
                {"type": "product", "id": 100, "meta": {"name": "X", "price": 1.0, "description": "d1"}},
                {"type": "faq",     "meta": {"question": "Q", "answer": "A"}}
            ]
    mgr.rag = DummyRag()

    class DummyLLM:
        def generate(self, prompt):
            return "LLM reply"
    mgr.llm = DummyLLM()

    conv_id, reply = await mgr.handle("dummy_session", user_id=1, conversation_id=None, message="hello")

    uuid.UUID(conv_id)
    assert reply == "LLM reply"
    assert cm_mod.ChatManager._recommendation_state[conv_id] == [100]

@pytest.mark.asyncio
async def test_more_flow(monkeypatch):
    mgr = ChatManager()
    conv = "conv-test"
    cm_mod.ChatManager._recommendation_state[conv] = [100]

    monkeypatch.setattr(cm_mod, "get_user", AsyncMock(return_value={"name": "Bob", "school_name": None}))
    monkeypatch.setattr(cm_mod, "get_conversation_history", AsyncMock(return_value=[]))
    monkeypatch.setattr(cm_mod, "add_message", AsyncMock())

    class DummyRag:
        def match_faq(self, message):
            return None
        def match_rule(self, message):
            return None
        def retrieve(self, query, top_k=None):
            return [
                {"type": "product", "id": 100, "meta": {"name": "X", "price": 1.0}},
                {"type": "product", "id": 200, "meta": {"name": "Y", "price": 2.0}}
            ]
    mgr.rag = DummyRag()

    conv_id, reply = await mgr.handle(
        "dummy_session",
        user_id=1,
        conversation_id=conv,
        message="more recommendations please"
    )

    assert conv_id == conv
    assert "- Y ($2.00)" in reply
    assert cm_mod.ChatManager._recommendation_state[conv] == [100, 200]