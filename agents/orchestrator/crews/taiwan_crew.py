"""Taiwan Planning Crew — itinerary, hotels, trains, festivals."""

from crewai import Crew

from orchestrator.agents.taiwan_festival import create_taiwan_festival_agent
from orchestrator.agents.taiwan_hotel import create_taiwan_hotel_agent
from orchestrator.agents.taiwan_itinerary import create_taiwan_itinerary_agent
from orchestrator.agents.taiwan_train import create_taiwan_train_agent
from orchestrator.tasks.planning_tasks import (
    create_festival_task,
    create_hotel_task,
    create_itinerary_task,
    create_train_task,
)


def create_taiwan_crew(slots: dict) -> Crew:
    itinerary_agent = create_taiwan_itinerary_agent()
    hotel_agent = create_taiwan_hotel_agent()
    train_agent = create_taiwan_train_agent()
    festival_agent = create_taiwan_festival_agent()

    return Crew(
        agents=[itinerary_agent, hotel_agent, train_agent, festival_agent],
        tasks=[
            create_itinerary_task(itinerary_agent, "Taiwan", slots),
            create_hotel_task(hotel_agent, "Taiwan", slots),
            create_train_task(train_agent, "Taiwan", slots),
            create_festival_task(festival_agent, "Taiwan", slots),
        ],
        verbose=True,
    )
