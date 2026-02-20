import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import DailyLimitError
from app.core.redis import get_redis
from app.models.usage import UsageRecord
from app.models.user import UserTier


async def get_usage_count(db: AsyncSession, user_id: uuid.UUID, today: date) -> int:
    # Try Redis first
    r = await get_redis()
    key = f"usage:{user_id}:{today.isoformat()}"
    count = await r.get(key)
    if count is not None:
        return int(count)

    # Fall back to DB
    stmt = select(UsageRecord).where(
        UsageRecord.user_id == user_id,
        UsageRecord.date == today,
    )
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    count = record.query_count if record else 0

    # Cache in Redis
    await r.set(key, count, ex=86400)
    return count


async def check_and_increment(db: AsyncSession, user_id: uuid.UUID, tier: UserTier) -> int:
    today = date.today()
    limit = settings.daily_limit_premium if tier == UserTier.premium else settings.daily_limit_free

    count = await get_usage_count(db, user_id, today)
    if count >= limit:
        raise DailyLimitError(
            f"Daily limit of {limit} AI queries reached. "
            f"{'Upgrade to premium for more.' if tier == UserTier.free else 'Try again tomorrow.'}"
        )

    # Increment in Redis
    r = await get_redis()
    key = f"usage:{user_id}:{today.isoformat()}"
    new_count = await r.incr(key)
    await r.expire(key, 86400)

    # Persist to DB
    stmt = select(UsageRecord).where(
        UsageRecord.user_id == user_id,
        UsageRecord.date == today,
    )
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()

    if record:
        record.query_count = new_count
    else:
        record = UsageRecord(user_id=user_id, date=today, query_count=new_count)
        db.add(record)

    await db.commit()
    return new_count
