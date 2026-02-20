"""Taiwan Travel MCP Server — 4 tools for Taiwan travel planning."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Taiwan Travel", host="0.0.0.0", port=8002)


@mcp.tool()
def search_taiwan_itinerary(
    city: str,
    duration: int,
    style: str = "balanced",
    budget_level: str = "medium",
    season: str = "autumn",
) -> dict:
    """Search for Taiwan itinerary suggestions."""
    itineraries = {
        "taipei": {
            "city": "Taipei",
            "suggestions": [
                {"theme": "Classic Taipei", "areas": ["Taipei 101", "Ximending", "Shilin Night Market", "Jiufen"]},
                {"theme": "Local Life", "areas": ["Dadaocheng", "Yongkang Street", "Maokong", "Beitou"]},
            ],
            "budget_per_day": {"low": 40, "medium": 80, "high": 180},
        },
        "tainan": {
            "city": "Tainan",
            "suggestions": [
                {"theme": "Heritage Walk", "areas": ["Anping Fort", "Confucius Temple", "Shennong Street"]},
                {"theme": "Food Trail", "areas": ["Hayashi Department Store", "Garden Night Market"]},
            ],
            "budget_per_day": {"low": 30, "medium": 60, "high": 120},
        },
        "hualien": {
            "city": "Hualien",
            "suggestions": [
                {"theme": "Taroko Gorge", "areas": ["Shakadang Trail", "Swallow Grotto", "Eternal Spring Shrine"]},
                {"theme": "Coastal", "areas": ["Qingshui Cliffs", "Shitiping", "East Coast"]},
            ],
            "budget_per_day": {"low": 35, "medium": 70, "high": 150},
        },
    }

    city_data = itineraries.get(city.lower(), itineraries["taipei"])
    daily_budget = city_data["budget_per_day"].get(budget_level, 80)

    return {
        "city": city_data["city"],
        "duration_days": duration,
        "style": style,
        "season": season,
        "daily_budget_usd": daily_budget,
        "total_budget_usd": daily_budget * duration,
        "itinerary_options": city_data["suggestions"],
        "season_tips": {
            "spring": "Comfortable but rainy. Bring umbrella.",
            "summer": "Very hot and humid. Typhoon season June-September.",
            "autumn": "Best season! October-November is perfect.",
            "winter": "Mild in south, cool in north. Great for hot springs.",
        }.get(season, ""),
    }


@mcp.tool()
def search_taiwan_hotels(
    city: str,
    checkin: str,
    checkout: str,
    guests: int = 2,
    budget: str = "medium",
) -> dict:
    """Search for hotels in Taiwanese cities."""
    hotels = {
        "taipei": [
            {"name": "Amba Taipei Songshan", "area": "Songshan", "price_per_night": 90, "rating": 4.4},
            {"name": "Hotel Proverbs Taipei", "area": "Da'an", "price_per_night": 150, "rating": 4.6},
            {"name": "Star Hostel Taipei", "area": "Station", "price_per_night": 20, "rating": 4.5},
            {"name": "Mandarin Oriental Taipei", "area": "Songshan", "price_per_night": 350, "rating": 4.9},
            {"name": "CityInn Hotel Taipei Station", "area": "Station", "price_per_night": 55, "rating": 4.2},
        ],
        "tainan": [
            {"name": "Silks Place Tainan", "area": "West Central", "price_per_night": 120, "rating": 4.5},
            {"name": "U.I.J Hotel", "area": "West Central", "price_per_night": 80, "rating": 4.4},
        ],
        "hualien": [
            {"name": "Taroko Village Hotel", "area": "Taroko", "price_per_night": 100, "rating": 4.3},
            {"name": "Kadda Hotel", "area": "Downtown", "price_per_night": 70, "rating": 4.2},
        ],
    }

    city_hotels = hotels.get(city.lower(), hotels["taipei"])
    budget_range = {"low": (0, 40), "medium": (40, 160), "high": (160, 1000)}
    min_p, max_p = budget_range.get(budget, (0, 1000))

    filtered = [h for h in city_hotels if min_p <= h["price_per_night"] <= max_p]

    return {
        "city": city,
        "checkin": checkin,
        "checkout": checkout,
        "guests": guests,
        "results": filtered or city_hotels[:2],
    }


@mcp.tool()
def search_taiwan_festivals(region: str, month: int, year: int = 2025) -> dict:
    """Search for festivals and events in Taiwan."""
    festivals = {
        "taipei": [
            {"month": 2, "name": "Taipei Lantern Festival", "location": "Various", "dates": "February"},
            {"month": 5, "name": "Dragon Boat Festival", "location": "Dajia Riverside", "dates": "May/June"},
            {"month": 10, "name": "Taipei Arts Festival", "location": "Various venues", "dates": "October"},
        ],
        "tainan": [
            {"month": 3, "name": "Yanshui Beehive Fireworks", "location": "Yanshui", "dates": "Lantern Festival"},
            {"month": 4, "name": "Mazu Pilgrimage", "location": "Dajia to Xingang", "dates": "March/April"},
        ],
        "hualien": [
            {"month": 7, "name": "Amis Harvest Festival", "location": "Various tribes", "dates": "July-August"},
        ],
        "pingxi": [
            {"month": 2, "name": "Pingxi Sky Lantern Festival", "location": "Pingxi", "dates": "Lantern Festival"},
        ],
    }

    region_festivals = festivals.get(region.lower(), [])
    monthly = [f for f in region_festivals if f["month"] == month]

    return {
        "region": region,
        "month": month,
        "year": year,
        "festivals": monthly or region_festivals,
    }


@mcp.tool()
def plan_taiwan_train_route(
    origin: str,
    destination: str,
    date: str,
    hsr: bool = True,
    tra: bool = True,
    passengers: int = 1,
) -> dict:
    """Plan a train route in Taiwan using HSR and TRA."""
    routes = {
        ("taipei", "taichung"): {"method": "HSR", "duration": "50m", "price_usd": 22, "hsr": True},
        ("taipei", "tainan"): {"method": "HSR", "duration": "1h 45m", "price_usd": 38, "hsr": True},
        ("taipei", "kaohsiung"): {"method": "HSR", "duration": "2h", "price_usd": 42, "hsr": True},
        ("taipei", "hualien"): {"method": "TRA Taroko Express", "duration": "2h 10m", "price_usd": 15, "hsr": False, "note": "Scenic east coast route. Book early!"},
        ("taipei", "jiufen"): {"method": "TRA + Bus", "duration": "1h 30m", "price_usd": 5, "hsr": False},
        ("taichung", "sun_moon_lake"): {"method": "Bus from HSR station", "duration": "1h 40m", "price_usd": 6, "hsr": False},
        ("kaohsiung", "kenting"): {"method": "Kenting Express Bus", "duration": "2h 30m", "price_usd": 12, "hsr": False},
        ("chiayi", "alishan"): {"method": "Alishan Forest Railway", "duration": "2h 30m", "price_usd": 13, "hsr": False, "note": "Scenic mountain railway. Limited seats."},
    }

    key = (origin.lower(), destination.lower())
    route = routes.get(key, {
        "method": "TRA",
        "duration": "varies",
        "price_usd": 15,
        "hsr": False,
    })

    total_price = route["price_usd"] * passengers

    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "route": route,
        "passengers": passengers,
        "total_price_usd": total_price,
        "tips": {
            "hsr_discount": "Early bird tickets save 10-35%",
            "tra_tip": "Reserve Taroko/Puyuma express trains early",
            "easycard": "EasyCard works on MRT, bus, and some TRA trains",
        },
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
