"""Currency Exchange Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_fast


def create_currency_exchange_agent() -> Agent:
    return Agent(
        role="Currency & Budget Advisor",
        goal="Convert budgets to local currency and provide money tips",
        backstory=(
            "You help travelers understand costs in local currencies and provide practical "
            "tips about money exchange, credit card acceptance, and tipping customs."
        ),
        llm=llm_fast,
        verbose=True,
    )
