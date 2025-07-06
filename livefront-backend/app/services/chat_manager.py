import uuid
from typing import Optional, Tuple, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import get_user, get_conversation_history, add_message
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService
from app.config import settings


class ChatManager:
    _recommendation_state: Dict[str, List[int]] = {}

    def __init__(self):
        self.rag = RAGService()
        self.llm = LLMService()

    async def initialize(self, session: AsyncSession):
        await self.rag.build_index(session)

    async def handle(self, session: AsyncSession, user_id: int, conversation_id: Optional[str], message: str) -> Tuple[str, str]:
        user = await get_user(session, user_id)
        if not user:
            raise ValueError("User not found")
        first = user["name"].split()[0]
        school = user.get("school_name")
        conv_id = conversation_id or str(uuid.uuid4())
        history = await get_conversation_history(session, conv_id)

        hits = self.rag.retrieve(message, top_k=settings.K_NEIGHBORS)
        history = await get_conversation_history(session, conv_id)

        faq_answer = self.rag.match_faq(message)
        if faq_answer:
            await add_message(session, user_id, conv_id, "user", message)
            await add_message(session, user_id, conv_id, "assistant", faq_answer)
            return conv_id, faq_answer

        rule_text = self.rag.match_rule(message)
        if rule_text:
            await add_message(session, user_id, conv_id, "user", message)
            await add_message(session, user_id, conv_id, "assistant", rule_text)
            return conv_id, rule_text
        
        hits = self.rag.retrieve(message, top_k=settings.K_NEIGHBORS)
        intent_hit = next(
            (
                h for h in hits
                if h["type"] == "intent" and h.get("score", 0) >= settings.INTENT_THRESHOLD
            ),
            None
        )
        if intent_hit:
            template = intent_hit["meta"]["response"]
            reply = template.format(name=first, school=school or "")
            await add_message(session, user_id, conv_id, "user", message)
            await add_message(session, user_id, conv_id, "assistant", reply)
            return conv_id, reply

        all_products = [h for h in hits if h["type"] == "product"]
        seen = ChatManager._recommendation_state.get(conv_id, [])
        text_lower = message.lower().strip()
        is_more = text_lower.startswith("more") or "more recommendation" in text_lower

        if is_more:
            remaining = [p for p in all_products if p["id"] not in seen]
            to_suggest = remaining[: settings.MORE_K]

            if not to_suggest:
                reply = (
                    "Looks like I’ve shared all the kid-friendly options I have. "
                    "Anything else I can help with?"
                )
            else:
                new_ids = [p["id"] for p in to_suggest]
                ChatManager._recommendation_state[conv_id] = seen + new_ids
                lines = [
                    f"- {p['meta']['name']} (${p['meta']['price']:.2f})"
                    for p in to_suggest
                ]
                reply = "Sure—here are a few more recommendations:\n" + "\n".join(lines)

            await add_message(session, user_id, conv_id, "user", message)
            await add_message(session, user_id, conv_id, "assistant", reply)
            return conv_id, reply

        to_suggest = all_products[: settings.DEFAULT_RECOMMEND_K]
        ChatManager._recommendation_state[conv_id] = seen + [p["id"] for p in to_suggest]

        ctx_lines: List[str] = []
        for p in to_suggest:
            prod = p["meta"]
            ctx_lines.append(
                f"- {prod['name']} (${prod['price']:.2f}): {prod.get('description','')}"
            )

        faq_hits = [h for h in hits if h["type"] == "faq"][: settings.DEFAULT_RECOMMEND_K]
        faq_ctx = [
            f"- Q: {f['meta']['question']}\n  A: {f['meta']['answer']}"
            for f in faq_hits
        ]

        if not ctx_lines and not faq_ctx:
            fallback = (
                "I’m sorry, I don’t have information on that topic. "
                "I can help you with products, our referral program, or FAQs—"
                "what would you like to discuss?"
            )
            await add_message(session, user_id, conv_id, "user", message)
            await add_message(session, user_id, conv_id, "assistant", fallback)
            return conv_id, fallback

        blocks = []
        if ctx_lines:
            blocks.append("[Products]\n" + "\n".join(ctx_lines))
        if faq_ctx:
            blocks.append("[FAQs]\n" + "\n".join(faq_ctx))
        context = "\n\n".join(blocks)

        hist_lines = []
        for turn in history[- settings.MAX_HISTORY :]:
            speaker = "User" if turn["role"] == "user" else "Assistant"
            hist_lines.append(f"{speaker}: {turn['content']}")
        history_block = "\n".join(hist_lines)

        sys_prompt = (
            f"You are Capper, the friendly AI assistant for Carton Caps. "
            f"Your role is to provide concise, helpful guidance about our products, referral "
            f"program, and frequently asked questions based on the specific knowledge provided. "
            f"Always focus your responses on these topics and avoid answering questions beyond this scope. "
            f"You are currently assisting {first}"
            + (f" who is associated with {school}." if school else ".")
            + f" When a user asks for product recommendations, pick the top {settings.DEFAULT_RECOMMEND_K} "
            f"products from the “[Products]” knowledge block and list them with name, price, and a one-sentence rationale. "
            f"If asked about other topics, politely guide them back to products, referrals, or FAQs."
        )

        prompt_parts = [
            sys_prompt,
            "[Relevant Knowledge]\n" + context
        ]
        if history_block:
            prompt_parts.append("[History]\n" + history_block)
        prompt_parts.append(f"User: {message}\nAssistant:")
        full_prompt = "\n\n".join(prompt_parts)

        try:
            full_reply = self.llm.generate(full_prompt)
        except Exception:
            full_reply = (
                "I'm sorry, I'm having trouble generating a response right now. "
                "Please try again in a moment or reach out to support@cartoncaps.com."
            )

        clean_reply = full_reply.split("\nUser:")[0].strip()

        await add_message(session, user_id, conv_id, "user", message)
        await add_message(session, user_id, conv_id, "assistant", clean_reply)
        return conv_id, clean_reply