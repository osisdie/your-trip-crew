from fastapi import APIRouter

from app.api.v1 import auth, chat, itineraries, packages, users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(packages.router, prefix="/packages", tags=["packages"])
api_router.include_router(itineraries.router, prefix="/itineraries", tags=["itineraries"])
