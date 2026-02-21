import uuid
from datetime import datetime

from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class TravelPackage(SQLModel, table=True):
    __tablename__ = "travel_packages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, index=True, max_length=200)
    destination: str = Field(max_length=100, index=True)
    category: str = Field(max_length=50, index=True)
    summary: str = Field(max_length=500)
    description: str
    duration_days: int
    price_usd: float
    cover_image_url: str | None = None
    highlights: list[str] | None = Field(default=None, sa_column=Column(JSON))
    translations: dict | None = Field(default=None, sa_column=Column(JSON))
    is_published: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

    # Relationships
    days: list["PackageDay"] = Relationship(back_populates="package")
    tags: list["PackageTag"] = Relationship(back_populates="package")


class PackageDay(SQLModel, table=True):
    __tablename__ = "package_days"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    package_id: uuid.UUID = Field(foreign_key="travel_packages.id", index=True)
    day_number: int
    title: str = Field(max_length=200)
    description: str
    activities: list[dict] | None = Field(default=None, sa_column=Column(JSON))
    translations: dict | None = Field(default=None, sa_column=Column(JSON))

    # Relationships
    package: TravelPackage = Relationship(back_populates="days")


class PackageTag(SQLModel, table=True):
    __tablename__ = "package_tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    package_id: uuid.UUID = Field(foreign_key="travel_packages.id", index=True)
    tag: str = Field(max_length=50, index=True)
    translations: dict | None = Field(default=None, sa_column=Column(JSON))

    # Relationships
    package: TravelPackage = Relationship(back_populates="tags")
