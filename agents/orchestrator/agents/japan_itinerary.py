"""Japan Itinerary Planner Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_reasoning


def create_japan_itinerary_agent() -> Agent:
    return Agent(
        role="Japan Itinerary Specialist",
        goal="Create detailed day-by-day Japan itineraries optimized for the traveler's preferences",
        backstory=(
            "You are a Japan travel expert who has lived in Japan for 10 years. "
            "You know every neighborhood in Tokyo, every temple in Kyoto, and every "
            "hidden gem across the country. You create itineraries that balance iconic "
            "sights with local experiences, always considering seasonal factors."
        ),
        llm=llm_reasoning,
        verbose=True,
    )
