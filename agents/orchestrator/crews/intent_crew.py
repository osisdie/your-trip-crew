"""Intent Crew — parses user messages into structured travel intent."""

from crewai import Crew

from orchestrator.agents.intent_parser import create_intent_parser
from orchestrator.tasks.intent_tasks import create_parse_intent_task


def create_intent_crew(user_message: str, existing_slots: dict | None = None) -> Crew:
    task = create_parse_intent_task(user_message, existing_slots)
    return Crew(
        agents=[create_intent_parser()],
        tasks=[task],
        verbose=True,
    )
