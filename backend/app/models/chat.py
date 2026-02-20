import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(default="New Chat", max_length=200)
    is_active: bool = Field(default=True)
    intent_slots: dict | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    # Relationships
    user: "User" = Relationship(back_populates="chat_sessions")  # noqa: F821
    messages: list["ChatMessage"] = Relationship(back_populates="session")


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="chat_sessions.id", index=True)
    role: MessageRole
    content: str
    metadata_: dict | None = Field(default=None, sa_column=Column("metadata", JSON))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    session: ChatSession = Relationship(back_populates="messages")
