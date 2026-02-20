import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.models.itinerary import ItineraryStatus


class ItineraryItemRead(BaseModel):
    id: uuid.UUID
    order: int
    time_start: str | None
    time_end: str | None
    category: str
    title: str
    description: str | None
    location: str | None
    lat: float | None
    lng: float | None
    cost_usd: float | None
    booking_url: str | None
    notes: str | None


class ItineraryDayRead(BaseModel):
    id: uuid.UUID
    day_number: int
    date: date | None
    city: str
    theme: str | None
    items: list[ItineraryItemRead]


class ItineraryListRead(BaseModel):
    id: uuid.UUID
    title: str
    destination: str
    start_date: date | None
    end_date: date | None
    duration_days: int
    num_travelers: int
    total_cost_usd: float | None
    status: ItineraryStatus
    created_at: datetime


class ItineraryDetailRead(ItineraryListRead):
    session_id: uuid.UUID | None
    cost_breakdown: dict | None
    days: list[ItineraryDayRead]


class ItineraryUpdate(BaseModel):
    status: ItineraryStatus | None = None
    title: str | None = None
