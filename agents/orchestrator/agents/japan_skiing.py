"""Japan Skiing Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_japan_skiing_agent(tools: list | None = None) -> Agent:
    return Agent(
        role="Japan Ski Resort Expert",
        goal="Recommend the best ski resorts and plan ski-focused itineraries",
        backstory=(
            "You are an expert on Japan's legendary powder snow. You know every resort "
            "from Niseko to Hakuba, which ones have the best kids' areas, the snow conditions "
            "by month, and how to combine skiing with onsen and local food experiences."
        ),
        llm=llm_fast,
        tools=tools or [],
        verbose=True,
    )
