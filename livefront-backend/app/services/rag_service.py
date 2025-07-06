import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import get_products, get_referral_faqs
from app.db.info import REFERRAL_FAQS, REFERRAL_RULES
from app.config import settings
import faiss

class RAGService:
    def __init__(self):
        self.embedder = SentenceTransformer(settings.EMBED_MODEL)
        self.embeddings: Optional[np.ndarray] = None
        self.corpus: List[Dict[str, Any]] = []

        self.faq_index = None
        self.rule_index = None

    async def build_index(self, session: AsyncSession):
        items = []

        prods = await get_products(session)
        for p in prods:
            txt = f"{p['name']}. {p.get('description','')}"
            items.append({'type': 'product', 'id': p['id'], 'text': txt, 'meta': p})

        faqs = await get_referral_faqs(session)
        for f in faqs:
            txt = f"{f['question']} {f['answer']}"
            items.append({'type': 'faq', 'id': f['id'], 'text': txt, 'meta': f})
        self.corpus = items
        if items:
            texts = [itm['text'] for itm in items]
            embs = self.embedder.encode(texts, convert_to_numpy=True)
            embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
            self.embeddings = embs

        faq_qs = [faq['question'] for faq in REFERRAL_FAQS]
        faq_embs = self.embedder.encode(faq_qs, convert_to_numpy=True)
        faiss.normalize_L2(faq_embs)
        dim = faq_embs.shape[1]
        self.faq_index = faiss.IndexFlatIP(dim)
        self.faq_index.add(faq_embs)

        rule_embs = self.embedder.encode(REFERRAL_RULES, convert_to_numpy=True)
        faiss.normalize_L2(rule_embs)
        self.rule_index = faiss.IndexFlatIP(dim)
        self.rule_index.add(rule_embs)
        
        intent_entries = [
            {
                "type": "intent",
                "id": "greeting",
                "text": "hello hi hey good morning good afternoon good evening how are you",
                "meta": {
                    "response": "Hi {name}! How can I assist you today?"
                }
            },
            {
                "type": "intent",
                "id": "capabilities",
                "text": "what can you help me with, how can you help, what do you do",
                "meta": {
                    "response": (
                        "**I can help you with:**\n"
                        "1. Find products – prices, descriptions, and recommendations.\n"
                        "2. Referral program – how it works, rewards, and rules.\n"
                        "3. FAQs – common questions about products, referrals, and more."
                    )
                }
            },
        ]
        items.extend(intent_entries)

        self.corpus = items
        texts = [item["text"] for item in items]
        embs = self.embedder.encode(texts, convert_to_numpy=True)
        embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
        self.embeddings = embs

    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        if self.embeddings is None:
            return []
        k = top_k or settings.K_NEIGHBORS
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
        sims = (self.embeddings @ q_emb[0])
        idxs = np.argsort(sims)[::-1][:k]
        results = []
        for i in idxs:
            itm = self.corpus[i].copy()
            itm['score'] = float(sims[i])
            results.append(itm)
        return results

    def match_faq(self, query: str, threshold: float = 0.65) -> Optional[str]:
        if self.faq_index is None:
            return None
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        D, I = self.faq_index.search(q_emb, 1)
        score = float(D[0][0]); idx = int(I[0][0])
        if score >= threshold:
            return REFERRAL_FAQS[idx]['answer']
        return None

    def match_rule(self, query: str, threshold: float = 0.65) -> Optional[str]:
        if self.rule_index is None:
            return None
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        D, I = self.rule_index.search(q_emb, 1)
        score = float(D[0][0]); idx = int(I[0][0])
        if score >= threshold:
            return REFERRAL_RULES[idx]
        return None