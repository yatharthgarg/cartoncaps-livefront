import numpy as np
from app.services.rag_service import RAGService

def test_rag_retrieve_similarity():
    service = RAGService()
    # manual corpus setup
    service.corpus = [
    {"type":"product","id":1,"text":"apple","meta":{}},
    {"type":"faq","id":2,"text":"banana","meta":{}}
    ]
    # create embeddings manually: apple->[1,0], banana->[0,1]
    service.embeddings = np.array([[1.0,0.0],[0.0,1.0]])
    # monkeypatch embedder.encode
    service.embedder.encode = lambda texts, convert_to_numpy: np.array([[1.0,0.0]])
    results = service.retrieve("apple", top_k=2)
    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2
    assert all("score" in r for r in results)