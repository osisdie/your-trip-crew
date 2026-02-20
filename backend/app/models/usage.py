import datetime
import uuid

from sqlalchemy import UniqueConstraint
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class UsageRecord(SQLModel, table=True):
    __tablename__ = "usage_records"
    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_user_date"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    date: datetime.date = Field(index=True)
    query_count: int = Field(default=0)
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    user: "User" = Relationship(back_populates="usage_records")  # noqa: F821
