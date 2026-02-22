"""Booking Crew — flights and eSIM."""

from crewai import Crew

from orchestrator.agents.esim_card import create_esim_agent
from orchestrator.agents.flight_booking import create_flight_booking_agent
from orchestrator.tasks.booking_tasks import create_esim_task, create_flight_task


def create_booking_crew(slots: dict, tools: list | None = None) -> Crew:
    flight_agent = create_flight_booking_agent(tools=tools)
    esim_agent = create_esim_agent(tools=tools)

    return Crew(
        agents=[flight_agent, esim_agent],
        tasks=[
            create_flight_task(flight_agent, slots),
            create_esim_task(esim_agent, slots),
        ],
        verbose=True,
    )
