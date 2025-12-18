from typing import Any

from fastapi import APIRouter, Depends, Query

from final_project.final_project.services.repo_service import RepositoryService
from final_project.final_project.web.api.deps import get_repository_service

router = APIRouter()


@router.get("/repos")
async def get_repositories(
    limit: int = Query(10),
    offset: int = Query(0),
    lang: str = Query(...),
    stars_min: int = Query(0),
    stars_max: int | None = Query(None),
    forks_min: int = Query(0),
    forks_max: int | None = Query(None),
    contributor: str | None = Query(None),
    repo_service: RepositoryService = Depends(get_repository_service),
) -> dict[str, Any]:
    """Export GitHub repositories to CSV using given filters."""
    filepath = await repo_service.fetch_and_save_repos(
        limit=limit,
        offset=offset,
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max,
        contributor=contributor,
    )
    return {"status": "success", "file_url": filepath}
