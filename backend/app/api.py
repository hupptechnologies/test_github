from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import AsyncSessionLocal
from .models import Message
from .schemas import ConversationRead, MessageRead

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get('/health')
async def health_check():
    return {"status": "ok", "message": "Backend is running"}

@router.get('/history', response_model=ConversationRead)
async def get_conversation_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        Message.__table__.select().order_by(Message.created_at.asc())
    )
    messages = result.fetchall()
    return {"messages": [MessageRead.from_orm(m) for m in [row for row in messages]]} 