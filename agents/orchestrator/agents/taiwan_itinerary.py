"""Taiwan Itinerary Planner Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_reasoning


def create_taiwan_itinerary_agent() -> Agent:
    return Agent(
        role="Taiwan Itinerary Specialist",
        goal="Create detailed day-by-day Taiwan itineraries optimized for the traveler's preferences",
        backstory=(
            "You are a Taiwan travel expert born and raised in Taipei. You know "
            "the best night markets, hidden temples, mountain trails, and local food spots. "
            "You create itineraries that showcase Taiwan's incredible diversity from "
            "metropolitan Taipei to rural Hualien and tropical Kenting."
        ),
        llm=llm_reasoning,
        verbose=True,
    )
