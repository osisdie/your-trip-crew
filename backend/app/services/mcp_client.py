"""Lightweight async MCP client using httpx.

Implements the MCP streamable-http protocol (initialize → notify → tools/call)
for calling MCP server tools from the backend orchestrator.

Uses httpx (already a backend dependency) — no new packages required.
"""

import asyncio
import json
import logging

import httpx

logger = logging.getLogger(__name__)

# JSON-RPC id counter (module-level, not critical to be thread-safe for our use)
_next_id = 0


def _rpc_id() -> int:
    global _next_id
    _next_id += 1
    return _next_id


def _parse_sse_result(text: str) -> dict | None:
    """Extract the JSON-RPC result from an SSE response body.

    SSE format: one or more `data: {...}` lines.  We want the last
    JSON-RPC message that has a "result" key.
    """
    for line in reversed(text.strip().splitlines()):
        line = line.strip()
        if not line.startswith("data:"):
            continue
        payload = line[len("data:") :].strip()
        if not payload or payload == "[DONE]":
            continue
        try:
            msg = json.loads(payload)
            if "result" in msg:
                return msg["result"]
        except (json.JSONDecodeError, TypeError):
            continue
    return None


async def call_mcp_tool(
    base_url: str,
    tool_name: str,
    arguments: dict | None = None,
) -> dict | None:
    """Call a single MCP tool via the streamable-http protocol.

    Lifecycle: initialize → notifications/initialized → tools/call.
    Returns the tool result dict, or None on any failure.
    """
    mcp_url = f"{base_url}/mcp"
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 1) Initialize
            init_resp = await client.post(
                mcp_url,
                headers=headers,
                json={
                    "jsonrpc": "2.0",
                    "id": _rpc_id(),
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "clientInfo": {"name": "trip-backend", "version": "1.0.0"},
                    },
                },
            )
            session_id = init_resp.headers.get("mcp-session-id")
            if session_id:
                headers["Mcp-Session-Id"] = session_id

            # 2) Notify initialized (fire-and-forget, no id field)
            await client.post(
                mcp_url,
                headers=headers,
                json={
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                },
            )

            # 3) Call the tool
            call_resp = await client.post(
                mcp_url,
                headers=headers,
                json={
                    "jsonrpc": "2.0",
                    "id": _rpc_id(),
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments or {},
                    },
                },
            )

            result = _parse_sse_result(call_resp.text)
            if result and "content" in result:
                # MCP tools/call wraps the return value in content[].text
                for item in result["content"]:
                    if item.get("type") == "text":
                        try:
                            return json.loads(item["text"])
                        except (json.JSONDecodeError, TypeError):
                            return {"raw": item["text"]}
            return result

    except Exception:
        logger.warning("MCP call failed: %s/%s", base_url, tool_name, exc_info=True)
        return None


async def call_mcp_tools_parallel(
    calls: list[tuple[str, str, dict]],
) -> list[dict | None]:
    """Call multiple MCP tools in parallel.

    Each element is (base_url, tool_name, arguments).
    Returns results in the same order. Failed calls return None.
    """
    if not calls:
        return []

    tasks = [call_mcp_tool(url, name, args) for url, name, args in calls]
    return list(await asyncio.gather(*tasks))
