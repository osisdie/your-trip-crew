"""Flight Search Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_flight_booking_agent(tools: list | None = None) -> Agent:
    return Agent(
        role="Flight Search Specialist",
        goal="Find the best flights for the trip based on dates, budget, and preferences",
        backstory=(
            "You are an expert at finding the best flight deals. You know which airlines "
            "serve which routes, optimal layover times, and how to balance price with "
            "convenience. You always present multiple options at different price points."
        ),
        llm=llm_fast,
        tools=tools or [],
        verbose=True,
    )
