"""Redis pub/sub event bus for real-time agent flow monitoring.

The orchestrator publishes step events via ``emit()``.  The SSE endpoint
subscribes via ``subscribe()`` and streams them to the browser.
"""

import asyncio
import json
import logging
import time
from collections.abc import AsyncGenerator

import redis.asyncio as aioredis

from app.config import settings
from app.core.redis import get_redis

logger = logging.getLogger(__name__)

CHANNEL_PREFIX = "flow"
SUBSCRIBE_TIMEOUT = 120  # seconds — prevents hanging connections


async def emit(
    session_id,
    *,
    step: str,
    crew: str | list[str] | None = None,
    status: str = "active",
    slots: dict | None = None,
    message: str = "",
) -> None:
    """Publish a flow event to the Redis channel for *session_id*."""
    r = await get_redis()
    payload = json.dumps(
        {
            "step": step,
            "crew": crew,
            "status": status,
            "slots": slots,
            "message": message,
            "ts": time.time(),
        },
        ensure_ascii=False,
    )
    channel = f"{CHANNEL_PREFIX}:{session_id}"
    await r.publish(channel, payload)
    logger.debug("flow_event %s → %s", channel, payload[:120])


async def subscribe(session_id) -> AsyncGenerator[str, None]:
    """Yield JSON event strings from the Redis channel for *session_id*.

    Terminates on ``complete`` / ``error`` steps or after *SUBSCRIBE_TIMEOUT*.
    The caller is responsible for closing the returned generator.

    A **dedicated** Redis connection is created because redis-py requires
    a connection in pub/sub mode to be exclusively used for subscriptions.
    """
    conn = aioredis.from_url(settings.redis_url, decode_responses=True)
    pubsub = conn.pubsub()
    channel = f"{CHANNEL_PREFIX}:{session_id}"

    try:
        await pubsub.subscribe(channel)
        deadline = asyncio.get_event_loop().time() + SUBSCRIBE_TIMEOUT

        while True:
            remaining = deadline - asyncio.get_event_loop().time()
            if remaining <= 0:
                logger.info("flow subscribe timeout for %s", session_id)
                break

            msg = await asyncio.wait_for(
                pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0),
                timeout=min(remaining, 5.0),
            )

            if msg is None:
                # No message yet — send SSE keep-alive comment
                yield ": keepalive\n\n"
                continue

            if msg["type"] != "message":
                continue

            data: str = msg["data"]
            yield f"data: {data}\n\n"

            # Stop streaming after terminal events
            try:
                parsed = json.loads(data)
                if parsed.get("step") in ("complete", "error"):
                    break
            except json.JSONDecodeError:
                pass

    except asyncio.TimeoutError:
        logger.info("flow subscribe timeout (outer) for %s", session_id)
    except asyncio.CancelledError:
        logger.debug("flow subscribe cancelled for %s", session_id)
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
        await conn.close()
