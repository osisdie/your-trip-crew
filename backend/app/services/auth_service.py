import uuid

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.user import User, UserOAuthAccount
from app.schemas.auth import TokenResponse


async def get_google_auth_url() -> str:
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    return f"https://accounts.google.com/o/oauth2/v2/auth?{qs}"


async def handle_google_callback(code: str, db: AsyncSession) -> TokenResponse:
    async with httpx.AsyncClient() as client:
        # Exchange code for tokens
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_resp.json()

        # Fetch user info
        userinfo_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        userinfo = userinfo_resp.json()

    return await _upsert_oauth_user(
        db=db,
        provider="google",
        provider_user_id=userinfo["id"],
        email=userinfo["email"],
        display_name=userinfo.get("name", userinfo["email"]),
        avatar_url=userinfo.get("picture"),
        access_token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
    )


async def get_line_auth_url() -> str:
    params = {
        "response_type": "code",
        "client_id": settings.line_channel_id,
        "redirect_uri": settings.line_redirect_uri,
        "scope": "profile openid email",
        "state": uuid.uuid4().hex,
    }
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    return f"https://access.line.me/oauth2/v2.1/authorize?{qs}"


async def handle_line_callback(code: str, db: AsyncSession) -> TokenResponse:
    async with httpx.AsyncClient() as client:
        # Exchange code for tokens
        token_resp = await client.post(
            "https://api.line.me/oauth2/v2.1/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.line_redirect_uri,
                "client_id": settings.line_channel_id,
                "client_secret": settings.line_channel_secret,
            },
        )
        token_data = token_resp.json()

        # Fetch profile
        profile_resp = await client.get(
            "https://api.line.me/v2/profile",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        profile = profile_resp.json()

    # LINE may not always return email; use userId as fallback
    email = token_data.get("email") or f"{profile['userId']}@line.user"

    return await _upsert_oauth_user(
        db=db,
        provider="line",
        provider_user_id=profile["userId"],
        email=email,
        display_name=profile.get("displayName", "LINE User"),
        avatar_url=profile.get("pictureUrl"),
        access_token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
    )


async def refresh_tokens(refresh_token_str: str, db: AsyncSession) -> TokenResponse:
    payload = decode_token(refresh_token_str)
    if payload is None or payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")

    user_id = uuid.UUID(payload["sub"])
    user = await db.get(User, user_id)
    if user is None or not user.is_active:
        raise ValueError("User not found")

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


async def _upsert_oauth_user(
    db: AsyncSession,
    provider: str,
    provider_user_id: str,
    email: str,
    display_name: str,
    avatar_url: str | None,
    access_token: str | None,
    refresh_token: str | None,
) -> TokenResponse:
    # Check if OAuth account exists
    stmt = select(UserOAuthAccount).where(
        UserOAuthAccount.provider == provider,
        UserOAuthAccount.provider_user_id == provider_user_id,
    )
    result = await db.execute(stmt)
    oauth_account = result.scalar_one_or_none()

    if oauth_account:
        # Update tokens
        oauth_account.access_token = access_token
        oauth_account.refresh_token = refresh_token
        user = await db.get(User, oauth_account.user_id)
    else:
        # Check if user exists by email
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                email=email,
                display_name=display_name,
                avatar_url=avatar_url,
            )
            db.add(user)
            await db.flush()

        oauth_account = UserOAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        db.add(oauth_account)

    await db.commit()

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
