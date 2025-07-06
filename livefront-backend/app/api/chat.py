import traceback
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.services.chat_manager import ChatManager

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str

chat_mgr = ChatManager()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, session: AsyncSession = Depends(get_db)):
    try:
        await chat_mgr.initialize(session)
        conv_id, reply = await chat_mgr.handle(
            session,
            req.user_id,
            req.conversation_id,
            req.message
        )
        return ChatResponse(conversation_id=conv_id, reply=reply)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")