import pytest
import torch
from app.services.llm_service import LLMService

class BadTokenizer:
    def __call__(self, *args, **kwargs):
        raise RuntimeError("boom")

@pytest.mark.asyncio
async def test_generate_fallback_on_error():
    svc = LLMService.__new__(LLMService)

    class BadTokenizer:
        def __call__(self, *args, **kwargs):
            raise RuntimeError("boom")

    svc.tokenizer = BadTokenizer()
    svc.model = None
    svc.device = torch.device("cpu")

    text = svc.generate("any prompt")
    assert "I'm sorry, I'm having trouble generating a response right now." in text