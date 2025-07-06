from typing import List, Optional, Dict, Any
from sqlalchemy import select, insert
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import (
    User, School, Product,
    ConversationHistory, ReferralFAQ
)

async def get_user(session: AsyncSession, user_id: int) -> Optional[Dict[str, Any]]:
    try:
        stmt = (
            select(User.id, User.name, School.name.label("school_name"))
            .join(School, User.school_id == School.id, isouter=True)
            .where(User.id == user_id)
        )
        res = await session.execute(stmt)
        row = res.mappings().first()
        return dict(row) if row else None
    except OperationalError:
        return None

async def get_products(session: AsyncSession) -> List[Dict[str, Any]]:
    try:
        stmt = select(Product.id, Product.name, Product.description, Product.price)
        res = await session.execute(stmt)
        return [dict(r) for r in res.mappings().all()]
    except OperationalError:
        return []

async def get_conversation_history(session: AsyncSession, conv_id: str) -> List[Dict[str, Any]]:
    try:
        stmt = (
            select(ConversationHistory)
            .where(ConversationHistory.conversation_id == conv_id)
            .order_by(ConversationHistory.timestamp)
        )
        res = await session.execute(stmt)
        records = res.scalars().all()
        return [
            {
                "role": "assistant" if r.sender == "assistant" else "user",
                "content": r.message
            }
            for r in records
        ]
    except OperationalError:
        return []

async def add_message(session: AsyncSession,user_id: int,conv_id: str,sender: str,message: str) -> None:
    try:
        now = __import__("datetime").datetime.utcnow()
        stmt = insert(ConversationHistory).values(
            user_id=user_id,
            conversation_id=conv_id,
            sender=sender,
            message=message,
            timestamp=now
        )
        await session.execute(stmt)
        await session.commit()
    except OperationalError:
        pass
    
async def get_all_users(session: AsyncSession) -> list[dict]:

    stmt = (
        select(
            User.id,
            User.name,
            School.name.label("school_name")
        )
        .join(School, User.school_id == School.id, isouter=True)
        .order_by(User.name)
    )
    res = await session.execute(stmt)
    return [ {"id": r.id, "name": r.name, "school_name": r.school_name} 
            for r in res.mappings().all() ]
    
async def get_referral_faqs(session: AsyncSession) -> list[dict]:
    """
    Fetch all referral FAQs for RAG context.
    """
    try:
        stmt = select(ReferralFAQ.id, ReferralFAQ.question, ReferralFAQ.answer)
        res = await session.execute(stmt)
        return [dict(r) for r in res.mappings().all()]
    except OperationalError:
        return []

async def get_all_users(session: AsyncSession) -> list[dict]:
    """
    Fetch all users (for the /users endpoint).
    """
    try:
        stmt = (
            select(User.id, User.name, School.name.label("school_name"))
            .join(School, User.school_id == School.id, isouter=True)
            .order_by(User.name)
        )
        res = await session.execute(stmt)
        return [
            {"id": r.id, "name": r.name, "school_name": r.school_name}
            for r in res.mappings().all()
        ]
    except OperationalError:
        return []