"""Task definitions for the Advisory Crew."""

from crewai import Task


def create_family_advice_task(agent, slots: dict) -> Task:
    return Task(
        description=(
            f"Provide family travel advice for {slots.get('destination', 'Japan')}.\n\n"
            f"- Children ages: {slots.get('children_ages', [])}\n"
            f"- Trip style: {slots.get('trip_style', 'balanced')}\n"
            f"- Duration: {slots.get('duration_days', 5)} days\n\n"
            f"Include safety tips, must-bring items, and age-appropriate activity suggestions."
        ),
        expected_output="Comprehensive family travel advice",
        agent=agent,
    )


def create_currency_task(agent, slots: dict) -> Task:
    dest_currency = {"japan": "JPY", "taiwan": "TWD"}.get(
        (slots.get("destination") or "japan").lower(), "JPY"
    )
    return Task(
        description=(
            f"Provide currency information for traveling to {slots.get('destination', 'Japan')}.\n\n"
            f"- Budget: ${slots.get('budget_usd', 1000)} USD\n"
            f"- Convert to {dest_currency}\n"
            f"- Provide daily spending estimates\n"
            f"- Include tipping and payment customs"
        ),
        expected_output="Currency conversion and money tips",
        agent=agent,
    )
