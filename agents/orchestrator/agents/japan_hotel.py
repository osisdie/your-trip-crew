"""Japan Hotel Search Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_japan_hotel_agent() -> Agent:
    return Agent(
        role="Japan Accommodation Finder",
        goal="Find the best hotels, ryokans, and hostels in Japan matching the traveler's budget and style",
        backstory=(
            "You specialize in Japanese accommodation from luxury ryokans with private onsen "
            "to budget-friendly capsule hotels. You know which neighborhoods are best for "
            "different types of travelers and which hotels offer the best value."
        ),
        llm=llm_fast,
        verbose=True,
    )
