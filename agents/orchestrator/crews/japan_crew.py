"""Japan Planning Crew — itinerary, hotels, trains, festivals, skiing."""

from crewai import Crew

from orchestrator.agents.japan_festival import create_japan_festival_agent
from orchestrator.agents.japan_hotel import create_japan_hotel_agent
from orchestrator.agents.japan_itinerary import create_japan_itinerary_agent
from orchestrator.agents.japan_skiing import create_japan_skiing_agent
from orchestrator.agents.japan_train import create_japan_train_agent
from orchestrator.tasks.planning_tasks import (
    create_festival_task,
    create_hotel_task,
    create_itinerary_task,
    create_ski_task,
    create_train_task,
)


def create_japan_crew(slots: dict, tools: list | None = None) -> Crew:
    itinerary_agent = create_japan_itinerary_agent(tools=tools)
    hotel_agent = create_japan_hotel_agent(tools=tools)
    train_agent = create_japan_train_agent(tools=tools)
    festival_agent = create_japan_festival_agent(tools=tools)

    agents = [itinerary_agent, hotel_agent, train_agent, festival_agent]
    tasks = [
        create_itinerary_task(itinerary_agent, "Japan", slots),
        create_hotel_task(hotel_agent, "Japan", slots),
        create_train_task(train_agent, "Japan", slots),
        create_festival_task(festival_agent, "Japan", slots),
    ]

    # Add skiing if requested
    if slots.get("has_skiing"):
        ski_agent = create_japan_skiing_agent(tools=tools)
        agents.append(ski_agent)
        tasks.append(create_ski_task(ski_agent, slots))

    return Crew(agents=agents, tasks=tasks, verbose=True)
