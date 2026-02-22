"""E2E tests for MCP server tool discovery and invocation.

Requires all MCP servers to be running (docker compose up -d).
Run via: make test-mcp
"""

import pytest

from tests.conftest import EXPECTED_TOOLS, call_mcp_tool, list_mcp_tools

# ── Tool Discovery ───────────────────────────────────────────────────────


class TestToolDiscovery:
    """Verify each MCP server exposes the expected tools."""

    @pytest.mark.asyncio
    async def test_japan_server_exposes_5_tools(self):
        names = await list_mcp_tools("japan")
        assert len(names) == 5
        for expected in EXPECTED_TOOLS["japan"]:
            assert expected in names

    @pytest.mark.asyncio
    async def test_taiwan_server_exposes_4_tools(self):
        names = await list_mcp_tools("taiwan")
        assert len(names) == 4
        for expected in EXPECTED_TOOLS["taiwan"]:
            assert expected in names

    @pytest.mark.asyncio
    async def test_flights_server_exposes_2_tools(self):
        names = await list_mcp_tools("flights")
        assert len(names) == 2
        for expected in EXPECTED_TOOLS["flights"]:
            assert expected in names

    @pytest.mark.asyncio
    async def test_utilities_server_exposes_3_tools(self):
        names = await list_mcp_tools("utilities")
        assert len(names) == 3
        for expected in EXPECTED_TOOLS["utilities"]:
            assert expected in names

    @pytest.mark.asyncio
    async def test_knowledge_server_exposes_3_tools(self):
        names = await list_mcp_tools("knowledge")
        assert len(names) == 3
        for expected in EXPECTED_TOOLS["knowledge"]:
            assert expected in names


# ── Japan Tool Invocation ────────────────────────────────────────────────


class TestJapanToolInvocation:
    """Verify Japan MCP tools return correct structured data."""

    @pytest.mark.asyncio
    async def test_search_itinerary_tokyo(self):
        result = await call_mcp_tool(
            "japan",
            "search_japan_itinerary",
            {"city": "Tokyo", "duration": 3, "season": "spring"},
        )
        assert result["city"] == "Tokyo"
        assert result["duration_days"] == 3
        assert result["daily_budget_usd"] > 0
        assert result["total_budget_usd"] == result["daily_budget_usd"] * 3
        assert len(result["itinerary_options"]) >= 1
        assert "cherry blossom" in result["season_tips"].lower()

    @pytest.mark.asyncio
    async def test_search_hotels_kyoto(self):
        result = await call_mcp_tool(
            "japan",
            "search_japan_hotels",
            {"city": "Kyoto", "checkin": "2025-04-01", "checkout": "2025-04-03", "budget": "high"},
        )
        assert result["city"] == "Kyoto"
        assert isinstance(result["results"], list)
        assert len(result["results"]) >= 1
        for hotel in result["results"]:
            assert "name" in hotel
            assert "price_per_night" in hotel

    @pytest.mark.asyncio
    async def test_search_festivals_kyoto_july(self):
        result = await call_mcp_tool(
            "japan",
            "search_japan_festivals",
            {"region": "Kyoto", "month": 7},
        )
        assert result["region"] == "Kyoto"
        assert result["month"] == 7
        festivals = result["festivals"]
        assert len(festivals) >= 1
        assert any("Gion" in f["name"] for f in festivals)

    @pytest.mark.asyncio
    async def test_plan_train_route_tokyo_kyoto(self):
        result = await call_mcp_tool(
            "japan",
            "plan_japan_train_route",
            {"origin": "Tokyo", "destination": "Kyoto", "date": "2025-04-01"},
        )
        assert result["origin"] == "Tokyo"
        assert result["destination"] == "Kyoto"
        assert "route" in result
        assert "Shinkansen" in result["route"]["method"]
        assert "jr_pass_info" in result

    @pytest.mark.asyncio
    async def test_search_ski_resorts_hokkaido(self):
        result = await call_mcp_tool(
            "japan",
            "search_japan_ski_resorts",
            {"region": "hokkaido", "skill_level": "intermediate"},
        )
        assert result["region"] == "hokkaido"
        resorts = result["resorts"]
        assert len(resorts) >= 1
        assert any("Niseko" in r["name"] for r in resorts)
        for resort in resorts:
            assert "daily_pass_usd" in resort
            assert "snow_quality" in resort


# ── Taiwan Tool Invocation ───────────────────────────────────────────────


class TestTaiwanToolInvocation:
    """Verify Taiwan MCP tools return correct structured data."""

    @pytest.mark.asyncio
    async def test_search_itinerary_taipei(self):
        result = await call_mcp_tool(
            "taiwan",
            "search_taiwan_itinerary",
            {"city": "Taipei", "duration": 4},
        )
        assert result["city"] == "Taipei"
        assert result["duration_days"] == 4
        assert result["daily_budget_usd"] > 0
        assert len(result["itinerary_options"]) >= 1

    @pytest.mark.asyncio
    async def test_search_hotels_taipei(self):
        result = await call_mcp_tool(
            "taiwan",
            "search_taiwan_hotels",
            {"city": "Taipei", "checkin": "2025-10-01", "checkout": "2025-10-04"},
        )
        assert result["city"] == "Taipei"
        assert isinstance(result["results"], list)
        assert len(result["results"]) >= 1

    @pytest.mark.asyncio
    async def test_search_festivals_taipei(self):
        result = await call_mcp_tool(
            "taiwan",
            "search_taiwan_festivals",
            {"region": "Taipei", "month": 2},
        )
        assert result["region"] == "Taipei"
        assert isinstance(result["festivals"], list)

    @pytest.mark.asyncio
    async def test_plan_train_route_taipei_tainan(self):
        result = await call_mcp_tool(
            "taiwan",
            "plan_taiwan_train_route",
            {"origin": "Taipei", "destination": "Tainan", "date": "2025-10-01"},
        )
        assert result["origin"] == "Taipei"
        assert result["destination"] == "Tainan"
        assert "route" in result


# ── Flights Tool Invocation ──────────────────────────────────────────────


class TestFlightsToolInvocation:
    """Verify Flights MCP tools return correct structured data."""

    @pytest.mark.asyncio
    async def test_search_flights_tpe_to_nrt(self):
        result = await call_mcp_tool(
            "flights",
            "search_flights",
            {"origin_iata": "TPE", "dest_iata": "NRT", "departure": "2025-04-01", "passengers": 2},
        )
        assert result["origin"] == "TPE"
        assert result["destination"] == "NRT"
        assert result["passengers"] == 2
        flights = result["results"]
        assert len(flights) >= 1
        for f in flights:
            assert f["total_price_usd"] == f["price_usd"] * 2

    @pytest.mark.asyncio
    async def test_get_flight_details(self):
        result = await call_mcp_tool(
            "flights",
            "get_flight_details",
            {"flight_id": "FL001"},
        )
        assert result["id"] == "FL001"
        assert result["airline"] == "Japan Airlines"
        assert "baggage" in result
        assert "amenities" in result
        assert "booking_url" in result

    @pytest.mark.asyncio
    async def test_search_flights_with_max_price(self):
        result = await call_mcp_tool(
            "flights",
            "search_flights",
            {"origin_iata": "TPE", "dest_iata": "NRT", "departure": "2025-04-01", "max_price": 260},
        )
        for f in result["results"]:
            assert f["price_usd"] <= 260


# ── Utilities Tool Invocation ────────────────────────────────────────────


class TestUtilitiesToolInvocation:
    """Verify Utilities MCP tools return correct structured data."""

    @pytest.mark.asyncio
    async def test_convert_currency_usd_to_jpy(self):
        result = await call_mcp_tool(
            "utilities",
            "convert_currency",
            {"amount": 100, "from_currency": "USD", "to_currency": "JPY"},
        )
        assert result["from_currency"] == "USD"
        assert result["to_currency"] == "JPY"
        assert result["original_amount"] == 100
        assert result["converted_amount"] == 15000.0  # 100 * 150
        assert result["rate"] == 150.0

    @pytest.mark.asyncio
    async def test_search_esim_plans_japan(self):
        result = await call_mcp_tool(
            "utilities",
            "search_esim_plans",
            {"country": "Japan", "duration_days": 7, "data_gb": 5.0},
        )
        assert result["country"] == "Japan"
        assert isinstance(result["plans"], list)
        assert len(result["plans"]) >= 1
        for plan in result["plans"]:
            assert "provider" in plan
            assert "price_usd" in plan

    @pytest.mark.asyncio
    async def test_family_travel_advice_japan(self):
        result = await call_mcp_tool(
            "utilities",
            "get_family_travel_advice",
            {"destination": "Japan", "children_ages": [3, 8]},
        )
        assert result["destination"] == "Japan"
        assert result["children_ages"] == [3, 8]
        assert len(result["general_tips"]) >= 1
        assert len(result["age_specific_advice"]) >= 1
        assert len(result["must_haves"]) >= 1
