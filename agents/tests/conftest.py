"""Shared fixtures for MCP E2E tests.

These tests run inside a Docker container on the same network as MCP servers.
Run via: make test-mcp
"""

import json
import os

import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# ─── MCP server URLs (same as orchestrator.mcp_config) ──────────────────
MCP_URLS = {
    "japan": os.getenv("MCP_JAPAN_URL", "http://trip-mcp-japan:8001/mcp"),
    "taiwan": os.getenv("MCP_TAIWAN_URL", "http://trip-mcp-taiwan:8002/mcp"),
    "flights": os.getenv("MCP_FLIGHTS_URL", "http://trip-mcp-flights:8003/mcp"),
    "utilities": os.getenv("MCP_UTILITIES_URL", "http://trip-mcp-utilities:8004/mcp"),
    "knowledge": os.getenv("MCP_KNOWLEDGE_URL", "http://trip-mcp-knowledge:8005/mcp"),
}

# Expected tool names per server
EXPECTED_TOOLS = {
    "japan": [
        "search_japan_itinerary",
        "search_japan_hotels",
        "search_japan_festivals",
        "search_japan_ski_resorts",
        "plan_japan_train_route",
    ],
    "taiwan": [
        "search_taiwan_itinerary",
        "search_taiwan_hotels",
        "search_taiwan_festivals",
        "plan_taiwan_train_route",
    ],
    "flights": [
        "search_flights",
        "get_flight_details",
    ],
    "utilities": [
        "convert_currency",
        "search_esim_plans",
        "get_family_travel_advice",
    ],
    "knowledge": [
        "semantic_search_packages",
        "query_knowledge_graph",
        "store_user_preference",
    ],
}


async def call_mcp_tool(server_key: str, tool_name: str, arguments: dict) -> dict | str:
    """Connect to an MCP server, invoke a tool, and return the parsed result.

    This is the core E2E helper — it opens a fresh MCP session, calls one tool,
    and returns the deserialized response. Used by both happy-path and edge-case tests.
    """
    url = MCP_URLS[server_key]
    async with streamablehttp_client(url=url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            text = result.content[0].text
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return text


async def list_mcp_tools(server_key: str) -> list[str]:
    """Connect to an MCP server and return the list of tool names."""
    url = MCP_URLS[server_key]
    async with streamablehttp_client(url=url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            return [t.name for t in tools_result.tools]


@pytest.fixture
def japan_url():
    return MCP_URLS["japan"]


@pytest.fixture
def taiwan_url():
    return MCP_URLS["taiwan"]


@pytest.fixture
def flights_url():
    return MCP_URLS["flights"]


@pytest.fixture
def utilities_url():
    return MCP_URLS["utilities"]
