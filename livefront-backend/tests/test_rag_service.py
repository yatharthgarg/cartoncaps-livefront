import pytest
from app.services.rag_service import RAGService

def test_retrieve_none_before_build():
    svc = RAGService()
    assert svc.retrieve("anything") == []

def test_match_faq_none_before_build():
    svc = RAGService()
    assert svc.match_faq("hi") is None

def test_match_rule_none_before_build():
    svc = RAGService()
    assert svc.match_rule("help") is None