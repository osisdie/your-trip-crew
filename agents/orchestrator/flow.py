"""TripPlanningFlow — CrewAI Flow that orchestrates all crews for trip planning.

Flow:
    User message → parse_intent → [router] → destination_crew → booking → advisory → synthesis
"""

import json
import logging

from crewai.flow.flow import Flow, listen, router, start

from orchestrator.crews.advisory_crew import create_advisory_crew
from orchestrator.crews.booking_crew import create_booking_crew
from orchestrator.crews.intent_crew import create_intent_crew
from orchestrator.crews.japan_crew import create_japan_crew
from orchestrator.crews.link_validator_crew import validate_links
from orchestrator.crews.synthesis_crew import create_synthesis_crew
from orchestrator.crews.taiwan_crew import create_taiwan_crew
from orchestrator.mcp_config import safe_mcp_tools
from orchestrator.state import IntentSlots, TripPlanningState

logger = logging.getLogger(__name__)


class TripPlanningFlow(Flow[TripPlanningState]):
    """Main orchestration flow for trip planning."""

    @start()
    def parse_intent(self):
        """Step 1: Parse user intent from the message."""
        logger.info("Parsing intent from: %s", self.state.user_message[:100])

        existing_slots = self.state.intent.model_dump(exclude_none=True) if self.state.intent else None
        crew = create_intent_crew(self.state.user_message, existing_slots)
        result = crew.kickoff()

        # Parse the result into IntentSlots
        try:
            result_text = str(result)
            # Try to extract JSON from the result
            if "{" in result_text:
                json_str = result_text[result_text.index("{") : result_text.rindex("}") + 1]
                parsed = json.loads(json_str)

                # Update intent slots
                for key, value in parsed.items():
                    if key in IntentSlots.model_fields and value is not None:
                        setattr(self.state.intent, key, value)

                # Check for clarifying questions
                if "clarifying_questions" in parsed:
                    self.state.clarifying_questions = parsed["clarifying_questions"]
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("Could not parse intent JSON: %s", e)

        self.state.slots_complete = self.state.intent.is_complete
        logger.info("Slots complete: %s, Intent: %s", self.state.slots_complete, self.state.intent)

    @router(parse_intent)
    def route_after_intent(self):
        """Route based on whether slots are complete."""
        if not self.state.slots_complete:
            return "ask_user"

        destination = (self.state.intent.destination or "").lower()
        if "japan" in destination:
            return "plan_japan"
        elif "taiwan" in destination:
            return "plan_taiwan"
        else:
            return "plan_japan"  # Default

    @listen("ask_user")
    def ask_clarifying_questions(self):
        """Generate clarifying questions for missing slots."""
        missing = self.state.intent.missing_fields
        if self.state.clarifying_questions:
            self.state.final_itinerary = "\n".join(self.state.clarifying_questions)
        else:
            questions = []
            if "destination" in missing:
                questions.append("Where would you like to go? We currently support Japan and Taiwan.")
            if "travel dates or duration" in missing:
                questions.append("When are you planning to travel, and for how many days?")
            if "number of travelers" in missing:
                questions.append("How many people will be traveling?")
            self.state.final_itinerary = (
                "\n".join(questions) if questions else "Could you tell me more about your trip plans?"
            )

    @listen("plan_japan")
    def plan_japan_trip(self):
        """Step 2a: Run Japan planning crew with MCP tools."""
        logger.info("Running Japan planning crew")
        slots = self.state.intent.model_dump(exclude_none=True)
        with safe_mcp_tools(["japan"]) as tools:
            crew = create_japan_crew(slots, tools=tools)
            result = crew.kickoff()
        self.state.itinerary_data = {"japan": str(result)}

    @listen("plan_taiwan")
    def plan_taiwan_trip(self):
        """Step 2b: Run Taiwan planning crew with MCP tools."""
        logger.info("Running Taiwan planning crew")
        slots = self.state.intent.model_dump(exclude_none=True)
        with safe_mcp_tools(["taiwan"]) as tools:
            crew = create_taiwan_crew(slots, tools=tools)
            result = crew.kickoff()
        self.state.itinerary_data = {"taiwan": str(result)}

    @listen(plan_japan_trip, plan_taiwan_trip)
    def book_flights_and_esim(self):
        """Step 3: Run booking crew with flights + utilities MCP tools."""
        logger.info("Running booking crew")
        slots = self.state.intent.model_dump(exclude_none=True)
        with safe_mcp_tools(["flights", "utilities"]) as tools:
            crew = create_booking_crew(slots, tools=tools)
            result = crew.kickoff()
        self.state.flight_data = {"results": str(result)}

    @listen(book_flights_and_esim)
    def get_advisory_info(self):
        """Step 4: Run advisory crew with utility MCP tools."""
        logger.info("Running advisory crew")
        slots = self.state.intent.model_dump(exclude_none=True)
        with safe_mcp_tools(["utilities"]) as tools:
            crew = create_advisory_crew(slots, tools=tools)
            result = crew.kickoff()
        self.state.currency_data = {"results": str(result)}

    @listen(get_advisory_info)
    def synthesize_final_itinerary(self):
        """Step 5: Synthesize everything into a final response."""
        logger.info("Running synthesis crew")

        # Build summary of all gathered data
        state_summary = (
            f"## Trip Intent\n{self.state.intent.model_dump_json(indent=2)}\n\n"
            f"## Itinerary Data\n{self.state.itinerary_data}\n\n"
            f"## Flight Data\n{self.state.flight_data}\n\n"
            f"## Currency & Advisory\n{self.state.currency_data}\n\n"
        )

        if self.state.family_advice:
            state_summary += f"## Family Advice\n{self.state.family_advice}\n\n"

        crew = create_synthesis_crew(state_summary)
        result = crew.kickoff()
        self.state.final_itinerary = str(result)

    @listen(synthesize_final_itinerary)
    def validate_links_step(self):
        """Step 6: Validate all URLs in the final itinerary."""
        logger.info("Validating links in final itinerary")
        if self.state.final_itinerary:
            self.state.final_itinerary = validate_links(self.state.final_itinerary)


async def run_trip_planning(
    user_message: str,
    user_id: str | None = None,
    session_id: str | None = None,
    existing_intent: dict | None = None,
) -> str:
    """Entry point for trip planning. Returns the final response."""
    state = TripPlanningState(
        user_id=user_id,
        session_id=session_id,
        user_message=user_message,
    )

    if existing_intent:
        for key, value in existing_intent.items():
            if key in IntentSlots.model_fields and value is not None:
                setattr(state.intent, key, value)

    flow = TripPlanningFlow()
    flow.state = state
    await flow.kickoff_async()

    return state.final_itinerary or "I'm sorry, I couldn't generate an itinerary. Please try again."
