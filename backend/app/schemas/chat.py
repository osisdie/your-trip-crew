import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.chat import MessageRole


class ChatSessionCreate(BaseModel):
    title: str | None = None


class ChatSessionRead(BaseModel):
    id: uuid.UUID
    title: str
    is_active: bool
    intent_slots: dict | None
    created_at: datetime
    updated_at: datetime


class ChatMessageCreate(BaseModel):
    content: str
    locale: str = "en"


class ChatMessageRead(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    role: MessageRole
    content: str
    metadata_: dict | None = None
    created_at: datetime


class ChatMessageList(BaseModel):
    messages: list[ChatMessageRead]
    total: int
    has_more: bool
