from __future__ import annotations

from fastapi import APIRouter

from homework_fastapi.web.v1.endpoints.repositories import router as repositories_router

api_router = APIRouter()
api_router.include_router(repositories_router, tags=["repositories"])
