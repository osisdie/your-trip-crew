import datetime
import uuid
from enum import Enum

from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class ItineraryStatus(str, Enum):
    draft = "draft"
    confirmed = "confirmed"


class Itinerary(SQLModel, table=True):
    __tablename__ = "itineraries"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    session_id: uuid.UUID | None = Field(default=None, foreign_key="chat_sessions.id")
    title: str = Field(max_length=200)
    destination: str = Field(max_length=100)
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    duration_days: int
    num_travelers: int = Field(default=1)
    total_cost_usd: float | None = None
    cost_breakdown: dict | None = Field(default=None, sa_column=Column(JSON))
    status: ItineraryStatus = Field(default=ItineraryStatus.draft)
    created_at: datetime.datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

    # Relationships
    user: "User" = Relationship(back_populates="itineraries")  # noqa: F821
    days: list["ItineraryDay"] = Relationship(back_populates="itinerary")


class ItineraryDay(SQLModel, table=True):
    __tablename__ = "itinerary_days"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    itinerary_id: uuid.UUID = Field(foreign_key="itineraries.id", index=True)
    day_number: int
    date: datetime.date | None = None
    city: str = Field(max_length=100)
    theme: str | None = Field(default=None, max_length=200)

    # Relationships
    itinerary: Itinerary = Relationship(back_populates="days")
    items: list["ItineraryItem"] = Relationship(back_populates="day")


class ItineraryItem(SQLModel, table=True):
    __tablename__ = "itinerary_items"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    day_id: uuid.UUID = Field(foreign_key="itinerary_days.id", index=True)
    order: int
    time_start: str | None = Field(default=None, max_length=10)
    time_end: str | None = Field(default=None, max_length=10)
    category: str = Field(max_length=50)  # transport, meal, activity, hotel
    title: str = Field(max_length=200)
    description: str | None = None
    location: str | None = Field(default=None, max_length=200)
    lat: float | None = None
    lng: float | None = None
    cost_usd: float | None = None
    booking_url: str | None = None
    notes: str | None = None

    # Relationships
    day: ItineraryDay = Relationship(back_populates="items")
