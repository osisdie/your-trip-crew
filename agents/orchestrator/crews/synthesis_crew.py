"""Synthesis Crew — assembles final itinerary from all gathered data."""

from crewai import Agent, Crew

from orchestrator.llm_config import llm_creative
from orchestrator.tasks.synthesis_tasks import create_synthesis_task


def create_synthesis_crew(state_summary: str) -> Crew:
    synthesis_agent = Agent(
        role="Travel Itinerary Writer",
        goal="Create a beautiful, comprehensive travel itinerary from all gathered data",
        backstory=(
            "You are a professional travel writer who creates stunning itineraries. "
            "You combine data from multiple sources — flights, hotels, activities, "
            "transport, and local tips — into a cohesive, inspiring travel plan. "
            "You write in the user's language and format everything beautifully."
        ),
        llm=llm_creative,
        verbose=True,
    )

    return Crew(
        agents=[synthesis_agent],
        tasks=[create_synthesis_task(synthesis_agent, state_summary)],
        verbose=True,
    )
