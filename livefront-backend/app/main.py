from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.models import Base
from app.api.users import router as users_router
from app.api.chat import router as chat_router
from app.db.database import engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.db.crud import get_user
from app.config import settings

app = FastAPI(title="Carton Caps AI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(chat_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables ensured, ready to serve.")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/welcome/{user_id}")
async def welcome(user_id: int, session: AsyncSession = Depends(lambda: AsyncSessionLocal())):
    """
    Returns the 3-line welcome (referral note, greeting, prompt).
    """
    user = await get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    first  = user["name"]
    school = user.get("school_name")
    greeting = (
        f"Hi {first}! I'm Capper, your personal Carton Caps assistant. "
        "Your purchases from us help to fund critical school programming efforts"
        + (f" for {school}." if school else ".") +
        f" Remember that a portion of your purchase goes to {school}!" if school else f" Remember that a portion of your purchase goes to your linked school!"
    )
    prompt = (
        "Ask me a question, and I'll do my best to help you. "
        "I'm currently equipped to help you with Carton Caps products, our referral program, and FAQs."
    )

    return {"messages": [greeting, prompt]}