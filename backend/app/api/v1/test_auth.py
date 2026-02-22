"""Debug-only endpoint: create a test user and return JWT tokens.

Gated behind settings.debug — returns 404 in production.
Used by Playwright E2E tests to bypass OAuth login flow.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.models.user import User, UserTier
from app.schemas.auth import TokenResponse

router = APIRouter()

TEST_USER_EMAIL = "e2e-test@trip-planner.local"


@router.post("/test-token", response_model=TokenResponse)
async def create_test_token(db: AsyncSession = Depends(get_db)):
    """Create (or fetch) a test user and return JWT tokens.

    Only available when DEBUG=true in .env.
    """
    if not settings.debug:
        from fastapi import HTTPException

        raise HTTPException(status_code=404)

    # Upsert test user
    result = await db.execute(select(User).where(User.email == TEST_USER_EMAIL))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email=TEST_USER_EMAIL,
            display_name="E2E Test User",
            tier=UserTier.premium,
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
