from pydantic import BaseModel
from datetime import datetime
from typing import List

class MessageBase(BaseModel):
    role: str  # 'user' or 'ai'
    content: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationRead(BaseModel):
    messages: List[MessageRead] 