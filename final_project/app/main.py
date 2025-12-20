import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.depends import (
    Stub,
    get_github_client,
    get_repository_service,
    get_settings,
)
from app.api.router import api_router
from app.infrastructure.github_client import GitHubClient
from app.services.repository_service import RepositoryService
from app.settings import Settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="GitHub Repository Search Service",
        description="Service for searching GitHub repositories and exporting to CSV",
        version="0.1.0",
    )

    app.dependency_overrides[Stub(Settings)] = get_settings
    app.dependency_overrides[Stub(GitHubClient)] = get_github_client
    app.dependency_overrides[Stub(RepositoryService)] = get_repository_service

    app.include_router(api_router)

    settings = get_settings()
    os.makedirs(settings.static_dir, exist_ok=True)
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

    return app


app = create_app()


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
