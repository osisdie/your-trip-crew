"""Tests for MCP error handling: invalid keys, unreachable servers, timeouts, unexpected input.

Tests in TestInvalidServerKeys and TestServerUnreachable do NOT require running MCP servers.
Tests in TestUnexpectedToolInput DO require running MCP servers.
Run via: make test-mcp
"""

import pytest

from orchestrator.mcp_config import MCP_SERVERS, safe_mcp_tools
from tests.conftest import call_mcp_tool


# ── Invalid Server Keys ──────────────────────────────────────────────────


class TestInvalidServerKeys:
    """safe_mcp_tools gracefully handles unknown/empty server keys."""

    def test_unknown_key_yields_empty(self):
        with safe_mcp_tools(["nonexistent"]) as tools:
            assert tools == []

    def test_all_unknown_keys_yields_empty(self):
        with safe_mcp_tools(["foo", "bar", "baz"]) as tools:
            assert tools == []

    def test_empty_keys_yields_empty(self):
        with safe_mcp_tools([]) as tools:
            assert tools == []


# ── Server Unreachable (connection refused) ──────────────────────────────


class TestServerUnreachable:
    """safe_mcp_tools gracefully degrades when servers can't be reached."""

    def test_connection_refused_yields_empty(self, monkeypatch):
        """Point to a port with nothing listening -> connection refused."""
        monkeypatch.setitem(
            MCP_SERVERS,
            "dead_server",
            {
                "url": "http://127.0.0.1:1/mcp",
                "transport": "streamable-http",
            },
        )
        with safe_mcp_tools(["dead_server"], connect_timeout=5) as tools:
            assert tools == []

    def test_unresolvable_host_yields_empty(self, monkeypatch):
        """Point to a hostname that doesn't resolve -> DNS error."""
        monkeypatch.setitem(
            MCP_SERVERS,
            "bad_dns",
            {
                "url": "http://this-host-does-not-exist.invalid:9999/mcp",
                "transport": "streamable-http",
            },
        )
        with safe_mcp_tools(["bad_dns"], connect_timeout=5) as tools:
            assert tools == []


# ── Connection Timeout ───────────────────────────────────────────────────


class TestConnectionTimeout:
    """safe_mcp_tools handles timeout when server doesn't respond."""

    def test_timeout_yields_empty(self, monkeypatch):
        """Non-routable IP causes connect timeout -> graceful degradation.

        Uses TEST-NET-1 (192.0.2.0/24, RFC 5737) which is guaranteed
        non-routable, causing a connect timeout rather than immediate refusal.
        """
        monkeypatch.setitem(
            MCP_SERVERS,
            "slow_server",
            {
                "url": "http://192.0.2.1:9999/mcp",
                "transport": "streamable-http",
            },
        )
        # Very short timeout so the test doesn't hang
        with safe_mcp_tools(["slow_server"], connect_timeout=2) as tools:
            assert tools == []


# ── Unexpected Tool Input (edge cases in MCP server responses) ───────────


class TestUnexpectedToolInput:
    """MCP tools handle invalid or edge-case inputs without crashing."""

    @pytest.mark.asyncio
    async def test_unknown_city_returns_fallback_data(self):
        """Unknown city -> server falls back to Tokyo data (not an error)."""
        result = await call_mcp_tool(
            "japan",
            "search_japan_itinerary",
            {"city": "Atlantis", "duration": 3},
        )
        # Server falls back to Tokyo when city is unknown
        assert result["city"] == "Tokyo"
        assert result["duration_days"] == 3
        assert result["daily_budget_usd"] > 0

    @pytest.mark.asyncio
    async def test_unknown_train_route_returns_generic(self):
        """Unknown route -> server returns generic JR Line fallback."""
        result = await call_mcp_tool(
            "japan",
            "plan_japan_train_route",
            {"origin": "Nagoya", "destination": "Kanazawa", "date": "2025-04-01"},
        )
        assert result["origin"] == "Nagoya"
        assert result["destination"] == "Kanazawa"
        assert result["route"]["method"] == "JR Line"
        assert result["route"]["duration"] == "varies"

    @pytest.mark.asyncio
    async def test_invalid_currency_returns_error(self):
        """Invalid currency code -> server returns error dict (not exception)."""
        result = await call_mcp_tool(
            "utilities",
            "convert_currency",
            {"amount": 100, "from_currency": "INVALID", "to_currency": "JPY"},
        )
        assert "error" in result
        assert "Unknown currency" in result["error"]

    @pytest.mark.asyncio
    async def test_nonexistent_flight_returns_error(self):
        """Invalid flight ID -> server returns error dict."""
        result = await call_mcp_tool(
            "flights",
            "get_flight_details",
            {"flight_id": "FAKE999"},
        )
        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_no_matching_flights_returns_empty(self):
        """Search for flights on nonexistent route -> empty results list."""
        result = await call_mcp_tool(
            "flights",
            "search_flights",
            {"origin_iata": "LAX", "dest_iata": "JFK", "departure": "2025-04-01"},
        )
        assert result["results"] == []

    @pytest.mark.asyncio
    async def test_unknown_esim_country_returns_empty(self):
        """Unknown country -> no matching plans."""
        result = await call_mcp_tool(
            "utilities",
            "search_esim_plans",
            {"country": "Antarctica", "duration_days": 7},
        )
        assert result["plans"] == []

    @pytest.mark.asyncio
    async def test_unknown_festival_region_returns_empty(self):
        """Unknown festival region -> empty festivals list."""
        result = await call_mcp_tool(
            "japan",
            "search_japan_festivals",
            {"region": "Atlantis", "month": 6},
        )
        assert result["festivals"] == []


# ── safe_mcp_tools Integration (CrewAI adapter layer) ────────────────────


class TestSafeMcpToolsIntegration:
    """Test the safe_mcp_tools wrapper with real MCP servers."""

    def test_single_server_loads_tools(self):
        """Verify safe_mcp_tools returns CrewAI tool objects."""
        with safe_mcp_tools(["japan"]) as tools:
            assert len(tools) == 5
            names = {t.name for t in tools}
            assert "search_japan_itinerary" in names

    def test_multiple_servers_aggregate_tools(self):
        """Verify safe_mcp_tools aggregates tools from multiple servers."""
        with safe_mcp_tools(["flights", "utilities"]) as tools:
            names = {t.name for t in tools}
            assert "search_flights" in names
            assert "convert_currency" in names
            assert len(tools) == 5  # 2 flights + 3 utilities

    def test_tools_have_name_and_description(self):
        """Verify each tool has the required CrewAI attributes."""
        with safe_mcp_tools(["utilities"]) as tools:
            for tool in tools:
                assert hasattr(tool, "name")
                assert hasattr(tool, "description")
                assert len(tool.name) > 0
                assert len(tool.description) > 0
