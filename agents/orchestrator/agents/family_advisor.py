"""Family Travel Advisor Agent."""

from crewai import Agent

from orchestrator.llm_config import llm_reasoning


def create_family_advisor_agent() -> Agent:
    return Agent(
        role="Family Travel Advisor",
        goal="Provide expert family travel advice tailored to children's ages and needs",
        backstory=(
            "You are a family travel specialist who has helped thousands of families "
            "travel with children of all ages. You know which attractions are stroller-friendly, "
            "which restaurants welcome kids, safety considerations, and how to pace an "
            "itinerary so everyone has fun without burnout."
        ),
        llm=llm_reasoning,
        verbose=True,
    )
