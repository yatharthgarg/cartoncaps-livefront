import pytest
import torch
from app.services.llm_service import LLMService

class DummyTokenizer:
    eos_token_id = 0
    pad_token_id = 0
    def __call__(self, prompt, return_tensors=None, truncation=None, max_length=None, padding=None):
        # just returns dummy input_ids tensor
        return {"input_ids": torch.tensor([[1, 2, 3]])}
    def decode(self, ids, skip_special_tokens=None):
        return "Hello response"

class DummyModel:
    def to(self, device): return self
    def eval(self): return self
    def generate(self, **kwargs):
        # simulate output token ids
        return torch.tensor([[1,2,3]])

@pytest.fixture(autouse=True)
def patch_transformers(monkeypatch):
    # Patch AutoTokenizer and AutoModelForCausalLM to use dummies
    monkeypatch.setattr(
        "app.services.llm_service.AutoTokenizer.from_pretrained",
        lambda name, use_fast=True: DummyTokenizer()
    )
    monkeypatch.setattr(
        "app.services.llm_service.AutoModelForCausalLM.from_pretrained",
        lambda name: DummyModel()
    )

def test_llm_generate_success():
    svc = LLMService()
    text = svc.generate("Hello")
    assert isinstance(text, str)
    assert "response" in text