import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user, get_db
from app.core.exceptions import NotFoundError
from app.models.itinerary import Itinerary, ItineraryDay
from app.models.user import User
from app.schemas.itinerary import ItineraryDetailRead, ItineraryListRead, ItineraryUpdate

router = APIRouter()


@router.get("", response_model=list[ItineraryListRead])
async def list_itineraries(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Itinerary)
        .where(Itinerary.user_id == user.id)
        .order_by(Itinerary.created_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{itinerary_id}", response_model=ItineraryDetailRead)
async def get_itinerary(
    itinerary_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Itinerary)
        .where(Itinerary.id == itinerary_id, Itinerary.user_id == user.id)
        .options(
            selectinload(Itinerary.days).selectinload(ItineraryDay.items)
        )
    )
    result = await db.execute(stmt)
    itinerary = result.scalar_one_or_none()
    if not itinerary:
        raise NotFoundError("Itinerary not found")
    return itinerary


@router.patch("/{itinerary_id}", response_model=ItineraryListRead)
async def update_itinerary(
    itinerary_id: uuid.UUID,
    body: ItineraryUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Itinerary).where(
        Itinerary.id == itinerary_id, Itinerary.user_id == user.id
    )
    result = await db.execute(stmt)
    itinerary = result.scalar_one_or_none()
    if not itinerary:
        raise NotFoundError("Itinerary not found")

    if body.status is not None:
        itinerary.status = body.status
    if body.title is not None:
        itinerary.title = body.title

    await db.commit()
    await db.refresh(itinerary)
    return itinerary


@router.delete("/{itinerary_id}")
async def delete_itinerary(
    itinerary_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Itinerary).where(
        Itinerary.id == itinerary_id, Itinerary.user_id == user.id
    )
    result = await db.execute(stmt)
    itinerary = result.scalar_one_or_none()
    if not itinerary:
        raise NotFoundError("Itinerary not found")

    await db.delete(itinerary)
    await db.commit()
    return {"message": "Itinerary deleted"}
