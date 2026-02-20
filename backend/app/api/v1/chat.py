import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.api.deps import get_current_user, get_db
from app.core.security import decode_token
from app.models.chat import MessageRole
from app.models.user import User
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageList,
    ChatMessageRead,
    ChatSessionCreate,
    ChatSessionRead,
)
from app.services import chat_service
from app.services.flow_events import subscribe as flow_subscribe
from app.services.orchestrator import process_user_message
from app.services.usage_service import check_and_increment

router = APIRouter()


@router.post("/sessions", response_model=ChatSessionRead)
async def create_session(
    body: ChatSessionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await chat_service.create_session(db, user.id, body.title)


@router.get("/sessions", response_model=list[ChatSessionRead])
async def list_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await chat_service.list_sessions(db, user.id)


@router.get("/sessions/{session_id}", response_model=ChatSessionRead)
async def get_session(
    session_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await chat_service.get_session(db, session_id, user.id)


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await chat_service.delete_session(db, session_id, user.id)
    return {"message": "Session deleted"}


@router.get("/sessions/{session_id}/messages", response_model=ChatMessageList)
async def get_messages(
    session_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify ownership
    await chat_service.get_session(db, session_id, user.id)
    messages, total = await chat_service.get_messages(db, session_id, limit, offset)
    return ChatMessageList(
        messages=[ChatMessageRead.model_validate(m, from_attributes=True) for m in messages],
        total=total,
        has_more=(offset + limit) < total,
    )


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageRead)
async def send_message(
    session_id: uuid.UUID,
    body: ChatMessageCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify ownership
    session = await chat_service.get_session(db, session_id, user.id)

    # Check daily limit
    await check_and_increment(db, user.id, user.tier)

    # Save user message
    await chat_service.add_message(db, session_id, MessageRole.user, body.content)

    # Process through agent orchestrator (returns visible reply + updated slots)
    assistant_content, updated_slots = await process_user_message(
        session_id=session_id,
        user_message=body.content,
        intent_slots=session.intent_slots,
    )

    # Persist accumulated intent slots back to the session
    await chat_service.update_intent_slots(db, session_id, updated_slots)

    # Save assistant response
    assistant_msg = await chat_service.add_message(
        db, session_id, MessageRole.assistant, assistant_content
    )

    return ChatMessageRead.model_validate(assistant_msg, from_attributes=True)


@router.get("/sessions/{session_id}/flow-events")
async def flow_events_sse(
    session_id: uuid.UUID,
    token: str = Query(..., description="JWT access token (EventSource can't send headers)"),
):
    """SSE stream of real-time agent flow events for a chat session."""
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token")

    return StreamingResponse(
        flow_subscribe(session_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable nginx buffering
        },
    )
