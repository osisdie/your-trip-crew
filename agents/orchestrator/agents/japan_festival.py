"""Japan Festival & Events Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_japan_festival_agent(tools: list | None = None) -> Agent:
    return Agent(
        role="Japan Festival Expert",
        goal="Find relevant festivals and seasonal events during the travel dates",
        backstory=(
            "You are deeply knowledgeable about Japan's rich festival calendar — from Gion "
            "Matsuri to Sapporo Snow Festival. You can identify which events coincide with "
            "travel dates and suggest itinerary adjustments to catch special events."
        ),
        llm=llm_fast,
        tools=tools or [],
        verbose=True,
    )
