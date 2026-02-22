"""Taiwan Hotel Search Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_taiwan_hotel_agent(tools: list | None = None) -> Agent:
    return Agent(
        role="Taiwan Accommodation Finder",
        goal="Find the best hotels and hostels in Taiwan matching the traveler's budget",
        backstory=(
            "You are an expert in Taiwanese accommodation ranging from boutique hotels "
            "in Taipei's Da'an district to cozy guesthouses near Taroko Gorge. You know "
            "which areas have the best transport connections and food options nearby."
        ),
        llm=llm_fast,
        tools=tools or [],
        verbose=True,
    )
