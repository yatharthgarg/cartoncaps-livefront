from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.db.crud import get_all_users

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/users")
async def list_users(session: AsyncSession = Depends(get_db)):
    users = await get_all_users(session)
    return users