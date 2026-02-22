"""MCP server configuration and tool loading for CrewAI agents."""

import logging
import os
from contextlib import contextmanager

from crewai_tools import MCPServerAdapter

logger = logging.getLogger(__name__)

# ─── MCP Server URLs (Docker-internal defaults) ────────────────────────
MCP_SERVERS: dict[str, dict] = {
    "japan": {
        "url": os.getenv("MCP_JAPAN_URL", "http://trip-mcp-japan:8001/mcp"),
        "transport": "streamable-http",
    },
    "taiwan": {
        "url": os.getenv("MCP_TAIWAN_URL", "http://trip-mcp-taiwan:8002/mcp"),
        "transport": "streamable-http",
    },
    "flights": {
        "url": os.getenv("MCP_FLIGHTS_URL", "http://trip-mcp-flights:8003/mcp"),
        "transport": "streamable-http",
    },
    "utilities": {
        "url": os.getenv("MCP_UTILITIES_URL", "http://trip-mcp-utilities:8004/mcp"),
        "transport": "streamable-http",
    },
    "knowledge": {
        "url": os.getenv("MCP_KNOWLEDGE_URL", "http://trip-mcp-knowledge:8005/mcp"),
        "transport": "streamable-http",
    },
}


@contextmanager
def safe_mcp_tools(server_keys: list[str], connect_timeout: int = 30):
    """Open MCP connections and yield CrewAI tool objects.

    On connection failure, logs a warning and yields an empty list
    so agents gracefully degrade to LLM-only reasoning.

    Args:
        server_keys: List of MCP server names (e.g. ["japan", "flights"]).
        connect_timeout: Seconds to wait for MCP server connection.
    """
    params_list = []
    for key in server_keys:
        if key not in MCP_SERVERS:
            logger.warning("Unknown MCP server key: %s", key)
            continue
        params_list.append(MCP_SERVERS[key])

    if not params_list:
        logger.warning("No valid MCP server keys provided: %s", server_keys)
        yield []
        return

    try:
        with MCPServerAdapter(params_list, connect_timeout=connect_timeout) as tools:
            logger.info(
                "MCP tools loaded from %s: %s",
                server_keys,
                [t.name for t in tools],
            )
            yield tools
    except Exception:
        logger.warning(
            "Failed to connect to MCP servers %s — falling back to LLM-only",
            server_keys,
            exc_info=True,
        )
        yield []
