"""Advisory Crew — family advice and currency info."""

from crewai import Crew

from orchestrator.agents.currency_exchange import create_currency_exchange_agent
from orchestrator.agents.family_advisor import create_family_advisor_agent
from orchestrator.tasks.advisory_tasks import create_currency_task, create_family_advice_task


def create_advisory_crew(slots: dict) -> Crew:
    agents = []
    tasks = []

    # Always include currency
    currency_agent = create_currency_exchange_agent()
    agents.append(currency_agent)
    tasks.append(create_currency_task(currency_agent, slots))

    # Add family advice if needed
    if slots.get("needs_family_advice") or slots.get("children_ages"):
        family_agent = create_family_advisor_agent()
        agents.append(family_agent)
        tasks.append(create_family_advice_task(family_agent, slots))

    return Crew(agents=agents, tasks=tasks, verbose=True)
