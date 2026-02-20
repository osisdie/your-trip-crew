import json
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.security import decode_token
from app.database import async_session
from app.models.chat import MessageRole
from app.services import chat_service
from app.services.orchestrator import process_user_message

router = APIRouter()


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: uuid.UUID, token: str | None = None):
    if not token:
        await websocket.close(code=4001, reason="Missing token")
        return

    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        await websocket.close(code=4001, reason="Invalid token")
        return

    user_id = uuid.UUID(payload["sub"])
    await websocket.accept()

    try:
        async with async_session() as db:
            # Verify session ownership
            session = await chat_service.get_session(db, session_id, user_id)

            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                user_content = message.get("content", "")

                if not user_content:
                    continue

                # Save user message
                await chat_service.add_message(db, session_id, MessageRole.user, user_content)

                # Send typing indicator
                await websocket.send_json({"type": "typing", "content": ""})

                # Process through orchestrator (returns tuple)
                response, updated_slots = await process_user_message(
                    session_id=session_id,
                    user_message=user_content,
                    intent_slots=session.intent_slots,
                )

                # Persist accumulated intent slots back to the session
                await chat_service.update_intent_slots(db, session_id, updated_slots)
                session.intent_slots = updated_slots  # keep local copy fresh

                # Save assistant message
                await chat_service.add_message(db, session_id, MessageRole.assistant, response)

                # Send slots update so the client can react
                await websocket.send_json({
                    "type": "slots_update",
                    "content": "",
                    "slots": updated_slots,
                })

                # Send response
                await websocket.send_json({"type": "message", "content": response})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "content": str(e)})
        await websocket.close()
