"""Flights MCP Server — 2 tools for flight search."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Flights", host="0.0.0.0", port=8003)

# Mock flight database
MOCK_FLIGHTS = [
    {
        "id": "FL001",
        "airline": "Japan Airlines",
        "code": "JL802",
        "origin": "TPE",
        "dest": "NRT",
        "departure": "08:30",
        "arrival": "12:30",
        "price_usd": 280,
        "cabin": "economy",
        "duration": "3h 0m",
    },
    {
        "id": "FL002",
        "airline": "ANA",
        "code": "NH852",
        "origin": "TPE",
        "dest": "NRT",
        "departure": "14:00",
        "arrival": "18:00",
        "price_usd": 310,
        "cabin": "economy",
        "duration": "3h 0m",
    },
    {
        "id": "FL003",
        "airline": "EVA Air",
        "code": "BR198",
        "origin": "TPE",
        "dest": "NRT",
        "departure": "10:00",
        "arrival": "14:10",
        "price_usd": 250,
        "cabin": "economy",
        "duration": "3h 10m",
    },
    {
        "id": "FL004",
        "airline": "China Airlines",
        "code": "CI100",
        "origin": "TPE",
        "dest": "NRT",
        "departure": "07:00",
        "arrival": "11:10",
        "price_usd": 240,
        "cabin": "economy",
        "duration": "3h 10m",
    },
    {
        "id": "FL005",
        "airline": "Peach Aviation",
        "code": "MM922",
        "origin": "TPE",
        "dest": "KIX",
        "departure": "06:00",
        "arrival": "09:30",
        "price_usd": 150,
        "cabin": "economy",
        "duration": "2h 30m",
    },
    {
        "id": "FL006",
        "airline": "Japan Airlines",
        "code": "JL814",
        "origin": "TPE",
        "dest": "KIX",
        "departure": "11:00",
        "arrival": "14:40",
        "price_usd": 290,
        "cabin": "economy",
        "duration": "2h 40m",
    },
    {
        "id": "FL007",
        "airline": "ANA",
        "code": "NH854",
        "origin": "NRT",
        "dest": "CTS",
        "departure": "09:00",
        "arrival": "10:40",
        "price_usd": 120,
        "cabin": "economy",
        "duration": "1h 40m",
    },
    {
        "id": "FL008",
        "airline": "Starlux Airlines",
        "code": "JX800",
        "origin": "TPE",
        "dest": "NRT",
        "departure": "09:15",
        "arrival": "13:20",
        "price_usd": 270,
        "cabin": "economy",
        "duration": "3h 5m",
    },
    {
        "id": "FL009",
        "airline": "Thai Airways",
        "code": "TG632",
        "origin": "BKK",
        "dest": "NRT",
        "departure": "07:35",
        "arrival": "15:45",
        "price_usd": 350,
        "cabin": "economy",
        "duration": "6h 10m",
    },
    {
        "id": "FL010",
        "airline": "Singapore Airlines",
        "code": "SQ636",
        "origin": "SIN",
        "dest": "NRT",
        "departure": "08:00",
        "arrival": "16:05",
        "price_usd": 400,
        "cabin": "economy",
        "duration": "7h 5m",
    },
]


@mcp.tool()
def search_flights(
    origin_iata: str,
    dest_iata: str,
    departure: str,
    return_date: str | None = None,
    passengers: int = 1,
    cabin: str = "economy",
    max_price: float | None = None,
) -> dict:
    """Search for flights between airports."""
    results = [
        f
        for f in MOCK_FLIGHTS
        if f["origin"] == origin_iata.upper() and f["dest"] == dest_iata.upper() and f["cabin"] == cabin
    ]

    if max_price is not None:
        results = [f for f in results if f["price_usd"] <= max_price]

    # Adjust prices for passengers
    for flight in results:
        flight["total_price_usd"] = flight["price_usd"] * passengers

    return {
        "origin": origin_iata,
        "destination": dest_iata,
        "departure_date": departure,
        "return_date": return_date,
        "passengers": passengers,
        "cabin": cabin,
        "results": sorted(results, key=lambda x: x["price_usd"]),
        "note": "Prices are estimates. Book through airline website for actual fares.",
    }


@mcp.tool()
def get_flight_details(flight_id: str) -> dict:
    """Get detailed information about a specific flight."""
    flight = next((f for f in MOCK_FLIGHTS if f["id"] == flight_id), None)
    if not flight:
        return {"error": "Flight not found"}

    return {
        **flight,
        "baggage": {"carry_on": "7kg", "checked": "23kg (1 piece)"},
        "amenities": ["In-flight entertainment", "Meal service", "USB charging"],
        "booking_url": f"https://example.com/book/{flight_id}",
        "cancellation_policy": "Free cancellation up to 24h before departure",
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
