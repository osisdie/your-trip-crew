from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.config import settings
from app.models.user import User, UserTier
from app.schemas.user import UsageRead, UserRead, UserUpdate
from app.services.usage_service import get_usage_count

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserRead)
async def update_me(
    body: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if body.display_name is not None:
        user.display_name = body.display_name
    if body.avatar_url is not None:
        user.avatar_url = body.avatar_url
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me/usage", response_model=UsageRead)
async def get_my_usage(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    today = date.today()
    count = await get_usage_count(db, user.id, today)
    limit = settings.daily_limit_premium if user.tier == UserTier.premium else settings.daily_limit_free
    return UsageRead(
        date=today.isoformat(),
        query_count=count,
        daily_limit=limit,
        remaining=max(0, limit - count),
    )
