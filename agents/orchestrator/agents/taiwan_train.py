"""Taiwan Train Route Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_taiwan_train_agent(tools: list | None = None) -> Agent:
    return Agent(
        role="Taiwan Rail Expert",
        goal="Plan optimal train routes using HSR and TRA",
        backstory=(
            "You know Taiwan's rail system inside out — High Speed Rail (HSR), "
            "Taiwan Railway Administration (TRA), and the famous Alishan Forest Railway. "
            "You help travelers navigate efficiently with EasyCard and early bird discounts."
        ),
        llm=llm_fast,
        tools=tools or [],
        verbose=True,
    )
