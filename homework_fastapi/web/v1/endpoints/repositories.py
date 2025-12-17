from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from homework_fastapi.services.repositories_service import RepositoriesService
from homework_fastapi.web.infrastructure.github_client import GitHubClientError

router = APIRouter()


@router.get("/repositories/search")
async def search_repositories(
    lang: str = Query(
        ..., min_length=1, description="Programming language of repositories"
    ),
    limit: int = Query(
        10, ge=1, le=1000, description="How many repositories to return"
    ),
    offset: int = Query(
        0, ge=0, description="Offset from the start of the search result"
    ),
    stars_min: int = Query(0, ge=0, description="Minimum stars"),
    stars_max: int | None = Query(None, ge=0, description="Maximum stars"),
    forks_min: int = Query(0, ge=0, description="Minimum forks"),
    forks_max: int | None = Query(None, ge=0, description="Maximum forks"),
) -> dict[str, object]:
    if stars_max is not None and stars_max < stars_min:
        raise HTTPException(status_code=422, detail="stars_max must be >= stars_min")
    if forks_max is not None and forks_max < forks_min:
        raise HTTPException(status_code=422, detail="forks_max must be >= forks_min")
    service = RepositoriesService()
    try:
        return await service.search_and_save_csv(
            lang=lang,
            limit=limit,
            offset=offset,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )
    except GitHubClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
