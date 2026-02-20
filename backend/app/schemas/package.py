import uuid
from datetime import datetime

from pydantic import BaseModel


class PackageDayRead(BaseModel):
    id: uuid.UUID
    day_number: int
    title: str
    description: str
    activities: list[dict] | None


class PackageTagRead(BaseModel):
    id: uuid.UUID
    tag: str


class PackageListRead(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    destination: str
    category: str
    summary: str
    duration_days: int
    price_usd: float
    cover_image_url: str | None
    highlights: list[str] | None


class PackageDetailRead(PackageListRead):
    description: str
    is_published: bool
    created_at: datetime
    days: list[PackageDayRead]
    tags: list[PackageTagRead]


class PackageFilterParams(BaseModel):
    destination: str | None = None
    category: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    min_duration: int | None = None
    max_duration: int | None = None
    limit: int = 20
    offset: int = 0
