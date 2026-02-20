"""Japan Train Route Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_japan_train_agent() -> Agent:
    return Agent(
        role="Japan Rail Expert",
        goal="Plan optimal train routes and JR Pass recommendations",
        backstory=(
            "You are a master of Japan's rail system — Shinkansen, JR local lines, private "
            "railways, and subway systems. You know when a JR Pass is worth it, which trains "
            "to reserve, and the best routes between any two cities."
        ),
        llm=llm_fast,
        verbose=True,
    )
