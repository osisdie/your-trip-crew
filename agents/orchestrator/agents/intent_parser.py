"""Intent Parser Agent — extracts travel intent slots from user messages."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_intent_parser() -> Agent:
    return Agent(
        role="Travel Intent Parser",
        goal="Extract structured travel intent from natural language user messages",
        backstory=(
            "You are an expert at understanding travel requests in multiple languages "
            "(English, Chinese, Japanese). You extract key information like destination, "
            "dates, budget, number of travelers, children ages, preferences, and trip style. "
            "When information is missing, you identify exactly what to ask."
        ),
        llm=llm_fast,
        verbose=True,
    )
