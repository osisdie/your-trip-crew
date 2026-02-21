"""State management for the TripPlanningFlow."""

from pydantic import BaseModel, Field


class IntentSlots(BaseModel):
    """Extracted travel intent from user messages."""

    destination: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    duration_days: int | None = None
    num_travelers: int | None = Field(default=None, ge=1)
    children_ages: list[int] | None = None
    budget_usd: float | None = None
    preferences: list[str] | None = None
    trip_style: str | None = None  # adventure, relaxation, culture, family, food
    origin_city: str | None = None
    has_skiing: bool = False
    needs_family_advice: bool = False

    @property
    def is_complete(self) -> bool:
        """Check if we have enough info to plan a trip."""
        return all(
            [
                self.destination,
                self.duration_days or (self.start_date and self.end_date),
                self.num_travelers,
            ]
        )

    @property
    def missing_fields(self) -> list[str]:
        """Return list of critical missing fields."""
        missing = []
        if not self.destination:
            missing.append("destination")
        if not self.duration_days and not (self.start_date and self.end_date):
            missing.append("travel dates or duration")
        if not self.num_travelers:
            missing.append("number of travelers")
        return missing


class TripPlanningState(BaseModel):
    """Full state carried through the planning flow."""

    # User context
    user_id: str | None = None
    session_id: str | None = None
    user_message: str = ""

    # Intent
    intent: IntentSlots = Field(default_factory=IntentSlots)
    slots_complete: bool = False

    # Intermediate results from crews
    itinerary_data: dict | None = None
    hotel_data: dict | None = None
    festival_data: dict | None = None
    ski_data: dict | None = None
    train_data: dict | None = None
    flight_data: dict | None = None
    esim_data: dict | None = None
    currency_data: dict | None = None
    family_advice: dict | None = None

    # Final output
    final_itinerary: str | None = None
    validated_itinerary: str | None = None
    cost_breakdown: dict | None = None
    clarifying_questions: list[str] | None = None
