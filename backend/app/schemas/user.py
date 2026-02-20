import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.user import UserTier


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str
    avatar_url: str | None
    tier: UserTier
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    display_name: str | None = None
    avatar_url: str | None = None


class UsageRead(BaseModel):
    date: str
    query_count: int
    daily_limit: int
    remaining: int
