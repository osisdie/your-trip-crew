"""Utilities MCP Server — 3 tools: currency, eSIM, family advice."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Utilities", host="0.0.0.0", port=8004)

# Mock exchange rates
EXCHANGE_RATES = {
    "USD": 1.0,
    "JPY": 150.0,
    "TWD": 32.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "THB": 35.0,
    "SGD": 1.34,
    "KRW": 1320.0,
    "CNY": 7.25,
    "HKD": 7.82,
}


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert between currencies with current exchange rates."""
    from_rate = EXCHANGE_RATES.get(from_currency.upper())
    to_rate = EXCHANGE_RATES.get(to_currency.upper())

    if from_rate is None or to_rate is None:
        return {"error": f"Unknown currency. Supported: {list(EXCHANGE_RATES.keys())}"}

    usd_amount = amount / from_rate
    converted = usd_amount * to_rate

    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "original_amount": amount,
        "converted_amount": round(converted, 2),
        "rate": round(to_rate / from_rate, 6),
        "note": "Rates are approximate. Check xe.com for live rates.",
    }


@mcp.tool()
def search_esim_plans(country: str, duration_days: int, data_gb: float = 5.0) -> dict:
    """Search for eSIM plans for a country."""
    plans = {
        "japan": [
            {"provider": "Ubigi", "data_gb": 3, "duration_days": 15, "price_usd": 9, "network": "SoftBank"},
            {"provider": "Airalo", "data_gb": 5, "duration_days": 30, "price_usd": 15, "network": "NTT Docomo"},
            {"provider": "Airalo", "data_gb": 10, "duration_days": 30, "price_usd": 25, "network": "NTT Docomo"},
            {"provider": "Sakura Mobile", "data_gb": -1, "duration_days": 30, "price_usd": 35, "network": "SoftBank", "note": "Unlimited data"},
        ],
        "taiwan": [
            {"provider": "Airalo", "data_gb": 3, "duration_days": 30, "price_usd": 8, "network": "Chunghwa Telecom"},
            {"provider": "Airalo", "data_gb": 5, "duration_days": 30, "price_usd": 12, "network": "Chunghwa Telecom"},
            {"provider": "Ubigi", "data_gb": 10, "duration_days": 30, "price_usd": 20, "network": "FarEasTone"},
        ],
    }

    country_plans = plans.get(country.lower(), [])
    suitable = [
        p for p in country_plans
        if (p["data_gb"] >= data_gb or p["data_gb"] == -1) and p["duration_days"] >= duration_days
    ]

    return {
        "country": country,
        "duration_days": duration_days,
        "data_gb_needed": data_gb,
        "plans": suitable or country_plans,
        "tip": "Install eSIM before departure. Most require QR code scanning.",
    }


@mcp.tool()
def get_family_travel_advice(
    destination: str,
    children_ages: list[int],
    style: str = "balanced",
    concerns: list[str] | None = None,
) -> dict:
    """Get family travel advice for a destination with children."""
    advice = {
        "japan": {
            "general": [
                "Japan is extremely family-friendly and safe",
                "Most train stations have elevators and baby facilities",
                "Convenience stores (konbini) have baby supplies 24/7",
                "Many restaurants have kids' menus (okosama set)",
            ],
            "by_age": {
                "toddler": [
                    "Bring a lightweight stroller — most places are stroller-accessible",
                    "Tokyo DisneySea has excellent toddler-friendly rides",
                    "Many malls have nursing rooms (junyushitsu)",
                ],
                "child": [
                    "Kids love the Shinkansen and can get window seats",
                    "Pokemon Centers and Ghibli Museum are hits",
                    "Most activities accept children from age 3-4",
                ],
                "teen": [
                    "Akihabara, Harajuku, and gaming arcades are teen favorites",
                    "Consider manga cafes and themed restaurants",
                    "Teens enjoy the independence of Japan's safe public transport",
                ],
            },
            "must_haves": ["Travel insurance", "Child-size masks", "Snacks from home", "Portable WiFi or eSIM"],
        },
        "taiwan": {
            "general": [
                "Taiwan is very safe and family-friendly",
                "Night markets are exciting for kids of all ages",
                "MRT is clean and efficient with priority seating",
                "Taiwanese people are very welcoming to families with children",
            ],
            "by_age": {
                "toddler": [
                    "Most MRT stations have lifts and baby changing facilities",
                    "Taipei Zoo is excellent for toddlers",
                    "Many family-friendly cafes with play areas",
                ],
                "child": [
                    "Night market games are a huge hit with kids",
                    "Leofoo Village theme park has a safari and rides",
                    "DIY activities like pineapple cake making",
                ],
                "teen": [
                    "Ximending is Taiwan's Harajuku — teens love it",
                    "Bubble tea culture is a fun experience",
                    "Jiufen's Spirited Away vibes appeal to anime fans",
                ],
            },
            "must_haves": ["Umbrella/rain gear", "Mosquito repellent", "Sun protection", "EasyCard for transport"],
        },
    }

    dest_advice = advice.get(destination.lower(), advice["japan"])

    # Categorize children
    age_categories = []
    for age in children_ages:
        if age <= 3:
            age_categories.append("toddler")
        elif age <= 12:
            age_categories.append("child")
        else:
            age_categories.append("teen")

    relevant_advice = []
    for cat in set(age_categories):
        relevant_advice.extend(dest_advice["by_age"].get(cat, []))

    return {
        "destination": destination,
        "children_ages": children_ages,
        "general_tips": dest_advice["general"],
        "age_specific_advice": relevant_advice,
        "must_haves": dest_advice["must_haves"],
        "concerns_addressed": {
            "safety": f"{destination} is one of the safest countries for families",
            "food": "Many options for picky eaters — rice, noodles, fried chicken are universal",
            "medical": "Pharmacies are widely available. Bring basic medicines from home.",
        },
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
