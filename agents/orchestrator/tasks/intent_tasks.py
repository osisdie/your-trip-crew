"""Task definitions for the Intent Crew."""

from crewai import Task

from orchestrator.agents.intent_parser import create_intent_parser


def create_parse_intent_task(user_message: str, existing_slots: dict | None = None) -> Task:
    """Create a task to parse user intent from a message."""
    context = f"Existing slots: {existing_slots}" if existing_slots else "No prior context."

    return Task(
        description=(
            f"Parse the following user message and extract travel intent slots.\n\n"
            f"User message: {user_message}\n\n"
            f"{context}\n\n"
            f"Extract these fields if mentioned:\n"
            f"- destination (Japan or Taiwan)\n"
            f"- start_date, end_date, duration_days\n"
            f"- num_travelers, children_ages\n"
            f"- budget_usd, trip_style, preferences\n"
            f"- origin_city, has_skiing, needs_family_advice\n\n"
            f"Return a JSON object with the extracted slots.\n"
            f"If critical info is missing, include a 'missing_fields' list and "
            f"'clarifying_questions' list in the response language matching the user's."
        ),
        expected_output="JSON with extracted intent slots and any clarifying questions",
        agent=create_intent_parser(),
    )
