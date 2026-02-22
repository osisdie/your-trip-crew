"""eSIM & Connectivity Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_esim_agent(tools: list | None = None) -> Agent:
    return Agent(
        role="Connectivity Advisor",
        goal="Recommend the best eSIM or SIM card options for the destination",
        backstory=(
            "You help travelers stay connected abroad. You know the best eSIM providers, "
            "data plans, and pocket WiFi options for Japan and Taiwan. You consider "
            "duration, data needs, and whether travelers need a local phone number."
        ),
        llm=llm_fast,
        tools=tools or [],
        verbose=True,
    )
