import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.chat import ChatMessage, ChatSession, MessageRole


async def create_session(db: AsyncSession, user_id: uuid.UUID, title: str | None = None) -> ChatSession:
    session = ChatSession(
        user_id=user_id,
        title=title or "New Chat",
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def list_sessions(db: AsyncSession, user_id: uuid.UUID) -> list[ChatSession]:
    stmt = (
        select(ChatSession)
        .where(ChatSession.user_id == user_id, ChatSession.is_active.is_(True))
        .order_by(ChatSession.updated_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> ChatSession:
    stmt = select(ChatSession).where(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id,
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundError("Chat session not found")
    return session


async def delete_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> None:
    session = await get_session(db, session_id, user_id)
    session.is_active = False
    await db.commit()


async def add_message(
    db: AsyncSession,
    session_id: uuid.UUID,
    role: MessageRole,
    content: str,
    metadata: dict | None = None,
) -> ChatMessage:
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        metadata_=metadata,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_messages(
    db: AsyncSession,
    session_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[ChatMessage], int]:
    # Count total
    from sqlalchemy import func

    count_stmt = select(func.count()).where(ChatMessage.session_id == session_id)
    total = (await db.execute(count_stmt)).scalar()

    # Fetch page
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def update_intent_slots(db: AsyncSession, session_id: uuid.UUID, slots: dict) -> ChatSession:
    session = await db.get(ChatSession, session_id)
    if not session:
        raise NotFoundError("Chat session not found")
    session.intent_slots = slots
    await db.commit()
    await db.refresh(session)
    return session
