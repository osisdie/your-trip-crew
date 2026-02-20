"""Task definitions for Planning Crews (Japan/Taiwan)."""

from crewai import Task


def create_itinerary_task(agent, destination: str, slots: dict) -> Task:
    return Task(
        description=(
            f"Create a detailed day-by-day itinerary for {destination}.\n\n"
            f"Trip details:\n"
            f"- Duration: {slots.get('duration_days', 5)} days\n"
            f"- Travelers: {slots.get('num_travelers', 2)}\n"
            f"- Style: {slots.get('trip_style', 'balanced')}\n"
            f"- Budget: ${slots.get('budget_usd', 'flexible')}\n"
            f"- Preferences: {slots.get('preferences', [])}\n\n"
            f"Include specific activities with times, restaurant suggestions, "
            f"and transport between locations."
        ),
        expected_output="Structured day-by-day itinerary with activities, times, and locations",
        agent=agent,
    )


def create_hotel_task(agent, destination: str, slots: dict) -> Task:
    return Task(
        description=(
            f"Find suitable hotels in {destination} for the trip.\n\n"
            f"- Duration: {slots.get('duration_days', 5)} nights\n"
            f"- Guests: {slots.get('num_travelers', 2)}\n"
            f"- Budget level: {'budget' if (slots.get('budget_usd', 0) or 0) < 1000 else 'medium'}\n"
            f"- Has children: {bool(slots.get('children_ages'))}\n\n"
            f"Return 2-3 hotel options per city in the itinerary."
        ),
        expected_output="Hotel recommendations with prices, locations, and ratings",
        agent=agent,
    )


def create_train_task(agent, destination: str, slots: dict) -> Task:
    return Task(
        description=(
            f"Plan train routes for the {destination} itinerary.\n\n"
            f"- Travelers: {slots.get('num_travelers', 2)}\n"
            f"- Include JR Pass / HSR pass recommendation\n"
            f"- Estimate transport costs between cities\n"
        ),
        expected_output="Train routes with durations, costs, and pass recommendations",
        agent=agent,
    )


def create_festival_task(agent, destination: str, slots: dict) -> Task:
    return Task(
        description=(
            f"Check for festivals and events in {destination} during the travel dates.\n\n"
            f"- Start date: {slots.get('start_date', 'flexible')}\n"
            f"- Duration: {slots.get('duration_days', 5)} days\n\n"
            f"Identify any events that could enhance or impact the trip."
        ),
        expected_output="List of relevant festivals/events with dates and locations",
        agent=agent,
    )


def create_ski_task(agent, slots: dict) -> Task:
    return Task(
        description=(
            f"Recommend ski resorts in Japan for the trip.\n\n"
            f"- Travelers: {slots.get('num_travelers', 2)}\n"
            f"- Children ages: {slots.get('children_ages', [])}\n"
            f"- Duration at resort: {slots.get('duration_days', 3)} days\n\n"
            f"Include lift pass costs, equipment rental, and family-friendly options."
        ),
        expected_output="Ski resort recommendations with costs and family info",
        agent=agent,
    )
