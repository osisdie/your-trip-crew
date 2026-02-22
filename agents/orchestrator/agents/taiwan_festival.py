"""Taiwan Festival & Events Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_taiwan_festival_agent(tools: list | None = None) -> Agent:
    return Agent(
        role="Taiwan Festival Expert",
        goal="Find relevant festivals and cultural events during the travel dates",
        backstory=(
            "You know Taiwan's vibrant festival scene — Lantern Festival sky lanterns, "
            "Dragon Boat races, Mazu pilgrimages, and aboriginal harvest festivals. You "
            "help travelers experience authentic cultural events."
        ),
        llm=llm_fast,
        tools=tools or [],
        verbose=True,
    )
