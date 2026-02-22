from fastapi import APIRouter

from app.api.v1 import auth, chat, itineraries, packages, users
from app.config import settings

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(packages.router, prefix="/packages", tags=["packages"])
api_router.include_router(itineraries.router, prefix="/itineraries", tags=["itineraries"])

# Debug-only: test token endpoint for E2E testing
if settings.debug:
    from app.api.v1 import test_auth

    api_router.include_router(test_auth.router, prefix="/auth", tags=["auth"])
