from fastapi import APIRouter

from app.api.endpoints import repositories

api_router = APIRouter(prefix="/api")
api_router.include_router(repositories.router)
