import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column as SAColumn
from sqlmodel import Column, DateTime, Field, SQLModel, func


class TravelEmbedding(SQLModel, table=True):
    __tablename__ = "travel_embeddings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_type: str = Field(max_length=50, index=True)  # "package", "itinerary", "knowledge"
    source_id: uuid.UUID = Field(index=True)
    content_text: str
    embedding: list[float] | None = Field(
        default=None,
        sa_column=SAColumn(Vector(1536)),
    )
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
