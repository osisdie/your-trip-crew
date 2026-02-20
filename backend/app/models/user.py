import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class UserTier(str, Enum):
    free = "free"
    premium = "premium"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    display_name: str = Field(max_length=100)
    avatar_url: str | None = None
    tier: UserTier = Field(default=UserTier.free)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    # Relationships
    oauth_accounts: list["UserOAuthAccount"] = Relationship(back_populates="user")
    chat_sessions: list["ChatSession"] = Relationship(back_populates="user")  # noqa: F821
    itineraries: list["Itinerary"] = Relationship(back_populates="user")  # noqa: F821
    usage_records: list["UsageRecord"] = Relationship(back_populates="user")  # noqa: F821


class UserOAuthAccount(SQLModel, table=True):
    __tablename__ = "user_oauth_accounts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    provider: str = Field(max_length=20)  # "google" | "line"
    provider_user_id: str = Field(index=True)
    access_token: str | None = None
    refresh_token: str | None = None
    token_expires_at: datetime | None = None
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    user: User = Relationship(back_populates="oauth_accounts")
