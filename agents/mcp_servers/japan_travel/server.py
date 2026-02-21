"""Japan Travel MCP Server — 5 tools for Japan travel planning."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Japan Travel", host="0.0.0.0", port=8001)


@mcp.tool()
def search_japan_itinerary(
    city: str,
    duration: int,
    style: str = "balanced",
    budget_level: str = "medium",
    season: str = "spring",
) -> dict:
    """Search for Japan itinerary suggestions based on city, duration, and preferences."""
    itineraries = {
        "tokyo": {
            "city": "Tokyo",
            "suggestions": [
                {
                    "theme": "Classic Tokyo",
                    "areas": ["Shibuya", "Asakusa", "Akihabara", "Shinjuku", "Harajuku"],
                },
                {
                    "theme": "Hidden Tokyo",
                    "areas": ["Yanaka", "Shimokitazawa", "Koenji", "Kagurazaka"],
                },
            ],
            "budget_per_day": {"low": 80, "medium": 150, "high": 300},
        },
        "kyoto": {
            "city": "Kyoto",
            "suggestions": [
                {
                    "theme": "Temple Trail",
                    "areas": ["Kiyomizu", "Fushimi Inari", "Arashiyama", "Gion"],
                },
                {
                    "theme": "Zen Experience",
                    "areas": ["Ryoan-ji", "Daitoku-ji", "Philosopher's Path"],
                },
            ],
            "budget_per_day": {"low": 70, "medium": 130, "high": 250},
        },
        "osaka": {
            "city": "Osaka",
            "suggestions": [
                {"theme": "Food Capital", "areas": ["Dotonbori", "Shinsekai", "Kuromon Market"]},
                {
                    "theme": "Culture & Fun",
                    "areas": ["Osaka Castle", "Universal Studios", "Sumiyoshi Taisha"],
                },
            ],
            "budget_per_day": {"low": 70, "medium": 140, "high": 280},
        },
    }

    city_data = itineraries.get(city.lower(), itineraries["tokyo"])
    daily_budget = city_data["budget_per_day"].get(budget_level, 150)

    return {
        "city": city_data["city"],
        "duration_days": duration,
        "style": style,
        "season": season,
        "daily_budget_usd": daily_budget,
        "total_budget_usd": daily_budget * duration,
        "itinerary_options": city_data["suggestions"],
        "season_tips": {
            "spring": "Cherry blossom season (late March-April). Book early!",
            "summer": "Hot and humid. Consider mountain areas.",
            "autumn": "Beautiful foliage (November). Very popular season.",
            "winter": "Great for skiing and onsen. Less crowded cities.",
        }.get(season, ""),
    }


@mcp.tool()
def search_japan_hotels(
    city: str,
    checkin: str,
    checkout: str,
    guests: int = 2,
    budget: str = "medium",
    style: str = "hotel",
) -> dict:
    """Search for hotels in Japanese cities."""
    hotels = {
        "tokyo": [
            {
                "name": "Hotel Gracery Shinjuku",
                "area": "Shinjuku",
                "price_per_night": 120,
                "style": "hotel",
                "rating": 4.3,
            },
            {
                "name": "Dormy Inn Premium Ginza",
                "area": "Ginza",
                "price_per_night": 95,
                "style": "hotel",
                "rating": 4.2,
            },
            {
                "name": "Nui. HOSTEL & BAR LOUNGE",
                "area": "Kuramae",
                "price_per_night": 35,
                "style": "hostel",
                "rating": 4.5,
            },
            {
                "name": "Hoshinoya Tokyo",
                "area": "Otemachi",
                "price_per_night": 450,
                "style": "ryokan",
                "rating": 4.8,
            },
        ],
        "kyoto": [
            {
                "name": "Hotel Kanra Kyoto",
                "area": "Gojo",
                "price_per_night": 180,
                "style": "hotel",
                "rating": 4.5,
            },
            {
                "name": "Ryokan Shimizu",
                "area": "Gion",
                "price_per_night": 250,
                "style": "ryokan",
                "rating": 4.7,
            },
            {
                "name": "Piece Hostel Sanjo",
                "area": "Sanjo",
                "price_per_night": 30,
                "style": "hostel",
                "rating": 4.4,
            },
        ],
        "osaka": [
            {
                "name": "Cross Hotel Osaka",
                "area": "Shinsaibashi",
                "price_per_night": 100,
                "style": "hotel",
                "rating": 4.3,
            },
            {
                "name": "Swissotel Nankai Osaka",
                "area": "Namba",
                "price_per_night": 200,
                "style": "hotel",
                "rating": 4.5,
            },
        ],
    }

    city_hotels = hotels.get(city.lower(), hotels["tokyo"])
    budget_range = {"low": (0, 60), "medium": (60, 200), "high": (200, 1000)}
    min_p, max_p = budget_range.get(budget, (0, 1000))

    filtered = [h for h in city_hotels if min_p <= h["price_per_night"] <= max_p]
    if style != "any":
        styled = [h for h in filtered if h["style"] == style]
        if styled:
            filtered = styled

    return {
        "city": city,
        "checkin": checkin,
        "checkout": checkout,
        "guests": guests,
        "results": filtered or city_hotels[:2],
    }


@mcp.tool()
def search_japan_festivals(region: str, month: int, year: int = 2025) -> dict:
    """Search for festivals and events in Japan by region and month."""
    festivals = {
        "tokyo": [
            {
                "month": 3,
                "name": "Cherry Blossom Festival",
                "location": "Ueno Park",
                "dates": "Late March - Early April",
            },
            {
                "month": 7,
                "name": "Sumida River Fireworks",
                "location": "Sumida River",
                "dates": "Last Saturday of July",
            },
            {
                "month": 11,
                "name": "Tori-no-Ichi Fair",
                "location": "Otori Shrine",
                "dates": "November",
            },
        ],
        "kyoto": [
            {"month": 4, "name": "Miyako Odori", "location": "Gion", "dates": "April 1-30"},
            {
                "month": 7,
                "name": "Gion Matsuri",
                "location": "Downtown Kyoto",
                "dates": "July 1-31",
            },
            {
                "month": 10,
                "name": "Jidai Matsuri",
                "location": "Imperial Palace",
                "dates": "October 22",
            },
        ],
        "hokkaido": [
            {
                "month": 2,
                "name": "Sapporo Snow Festival",
                "location": "Odori Park",
                "dates": "Early February",
            },
            {
                "month": 7,
                "name": "Furano Lavender Festival",
                "location": "Farm Tomita",
                "dates": "July",
            },
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
def search_japan_ski_resorts(
    region: str = "hokkaido",
    skill_level: str = "intermediate",
    has_kids_area: bool = False,
    dates: str = "",
) -> dict:
    """Search for ski resorts in Japan."""
    resorts = [
        {
            "name": "Niseko Grand Hirafu",
            "region": "hokkaido",
            "skill_levels": ["beginner", "intermediate", "advanced"],
            "has_kids_area": True,
            "daily_pass_usd": 65,
            "snow_quality": "legendary powder",
        },
        {
            "name": "Niseko Village",
            "region": "hokkaido",
            "skill_levels": ["intermediate", "advanced"],
            "has_kids_area": True,
            "daily_pass_usd": 60,
            "snow_quality": "legendary powder",
        },
        {
            "name": "Furano",
            "region": "hokkaido",
            "skill_levels": ["beginner", "intermediate", "advanced"],
            "has_kids_area": True,
            "daily_pass_usd": 50,
            "snow_quality": "excellent powder",
        },
        {
            "name": "Hakuba Valley",
            "region": "nagano",
            "skill_levels": ["intermediate", "advanced"],
            "has_kids_area": True,
            "daily_pass_usd": 55,
            "snow_quality": "great powder",
        },
        {
            "name": "Nozawa Onsen",
            "region": "nagano",
            "skill_levels": ["beginner", "intermediate", "advanced"],
            "has_kids_area": False,
            "daily_pass_usd": 45,
            "snow_quality": "excellent",
        },
        {
            "name": "Myoko Kogen",
            "region": "niigata",
            "skill_levels": ["beginner", "intermediate"],
            "has_kids_area": True,
            "daily_pass_usd": 40,
            "snow_quality": "deep snow",
        },
    ]

    filtered = resorts
    if region:
        region_filtered = [r for r in filtered if r["region"] == region.lower()]
        if region_filtered:
            filtered = region_filtered
    if has_kids_area:
        filtered = [r for r in filtered if r["has_kids_area"]]
    filtered = [r for r in filtered if skill_level in r["skill_levels"]]

    return {
        "region": region,
        "skill_level": skill_level,
        "has_kids_area": has_kids_area,
        "dates": dates,
        "resorts": filtered or resorts[:3],
    }


@mcp.tool()
def plan_japan_train_route(
    origin: str,
    destination: str,
    date: str,
    jr_pass: bool = True,
    passengers: int = 1,
) -> dict:
    """Plan a train route in Japan using JR and other rail systems."""
    routes = {
        ("tokyo", "kyoto"): {
            "method": "Shinkansen Nozomi",
            "duration": "2h 15m",
            "price_usd": 120,
            "jr_pass_covered": True,
            "note": "Nozomi not covered by JR Pass, use Hikari instead (2h 40m)",
        },
        ("tokyo", "osaka"): {
            "method": "Shinkansen Nozomi",
            "duration": "2h 30m",
            "price_usd": 130,
            "jr_pass_covered": True,
        },
        ("tokyo", "hakone"): {
            "method": "Odakyu Romance Car",
            "duration": "1h 25m",
            "price_usd": 18,
            "jr_pass_covered": False,
        },
        ("tokyo", "nikko"): {
            "method": "Tobu Railway",
            "duration": "2h",
            "price_usd": 25,
            "jr_pass_covered": False,
        },
        ("kyoto", "nara"): {
            "method": "JR Nara Line",
            "duration": "45m",
            "price_usd": 7,
            "jr_pass_covered": True,
        },
        ("osaka", "kyoto"): {
            "method": "JR Special Rapid",
            "duration": "30m",
            "price_usd": 5,
            "jr_pass_covered": True,
        },
        ("tokyo", "hiroshima"): {
            "method": "Shinkansen Nozomi",
            "duration": "4h",
            "price_usd": 170,
            "jr_pass_covered": True,
        },
        ("tokyo", "sapporo"): {
            "method": "Shinkansen + Hokkaido Shinkansen",
            "duration": "8h",
            "price_usd": 250,
            "jr_pass_covered": True,
            "note": "Consider flying (1.5h, ~$100)",
        },
    }

    key = (origin.lower(), destination.lower())
    route = routes.get(
        key,
        {
            "method": "JR Line",
            "duration": "varies",
            "price_usd": 50,
            "jr_pass_covered": True,
        },
    )

    total_price = route["price_usd"] * passengers
    if jr_pass and route.get("jr_pass_covered"):
        total_price = 0  # Covered by JR Pass

    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "route": route,
        "passengers": passengers,
        "jr_pass": jr_pass,
        "total_price_usd": total_price,
        "jr_pass_info": {
            "7_day_price": 230,
            "14_day_price": 370,
            "21_day_price": 470,
            "note": "JR Pass covers most JR trains including Shinkansen (except Nozomi/Mizuho)",
        },
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
