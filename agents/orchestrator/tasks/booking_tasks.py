"""Task definitions for the Booking Crew."""

from crewai import Task


def create_flight_task(agent, slots: dict) -> Task:
    return Task(
        description=(
            f"Search for flights to {slots.get('destination', 'Japan')}.\n\n"
            f"- Origin: {slots.get('origin_city', 'TPE')}\n"
            f"- Dates: {slots.get('start_date', 'flexible')} to {slots.get('end_date', 'flexible')}\n"
            f"- Passengers: {slots.get('num_travelers', 2)}\n"
            f"- Budget: ${slots.get('budget_usd', 'flexible')}\n\n"
            f"Return 3-5 best flight options sorted by value."
        ),
        expected_output="Flight options with prices, airlines, and durations",
        agent=agent,
    )


def create_esim_task(agent, slots: dict) -> Task:
    return Task(
        description=(
            f"Find eSIM plans for {slots.get('destination', 'Japan')}.\n\n"
            f"- Duration: {slots.get('duration_days', 5)} days\n"
            f"- Travelers: {slots.get('num_travelers', 2)}\n\n"
            f"Recommend the best data plan options."
        ),
        expected_output="eSIM recommendations with prices and coverage",
        agent=agent,
    )
