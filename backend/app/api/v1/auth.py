from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError

from app.api.deps import get_db
from app.config import settings
from app.schemas.auth import TokenRefreshRequest, TokenResponse
from app.services.auth_service import (
    get_google_auth_url,
    get_line_auth_url,
    handle_google_callback,
    handle_line_callback,
    refresh_tokens,
)

router = APIRouter()


@router.get("/google")
async def google_login():
    url = await get_google_auth_url()
    return RedirectResponse(url=url)


@router.get("/google/callback")
async def google_callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    token_response = await handle_google_callback(code, db)
    redirect_url = (
        f"{settings.frontend_url}/auth/callback"
        f"?access_token={token_response.access_token}"
        f"&refresh_token={token_response.refresh_token}"
    )
    return RedirectResponse(url=redirect_url)


@router.get("/line")
async def line_login():
    url = await get_line_auth_url()
    return RedirectResponse(url=url)


@router.get("/line/callback")
async def line_callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    token_response = await handle_line_callback(code, db)
    redirect_url = (
        f"{settings.frontend_url}/auth/callback"
        f"?access_token={token_response.access_token}"
        f"&refresh_token={token_response.refresh_token}"
    )
    return RedirectResponse(url=redirect_url)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await refresh_tokens(body.refresh_token, db)
    except (ValueError, Exception):
        raise UnauthorizedError("Invalid or expired refresh token")


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
