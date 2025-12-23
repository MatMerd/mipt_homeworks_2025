from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from starlette import status

from github_stars.services.github_repos.service import (
    GitHubReposExportService,
    RepoSearchParams,
    SortField,
    SortOrder,
)

router = APIRouter()


def get_export_service(request: Request) -> GitHubReposExportService:
    """Get GitHubReposExportService instance from the FastAPI application state."""
    svc = getattr(request.app.state, "github_repos_export_service", None)
    if svc is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GitHubReposExportService is not wired",
        )
    return svc


def get_repo_search_params(
    limit: int = Query(..., ge=0),
    offset: int = Query(0, ge=0),
    lang: str = Query(..., min_length=1),
    topics: list[str] = Query(default_factory=list),
    stars_min: int = Query(0, ge=0),
    stars_max: int | None = Query(None, ge=0),
    forks_min: int = Query(0, ge=0),
    forks_max: int | None = Query(None, ge=0),
    sort: SortField = Query("stars"),
    order: SortOrder = Query("desc"),
) -> RepoSearchParams:
    """Parse query parameters into RepoSearchParams (including topics)."""
    return RepoSearchParams(
        limit=limit,
        offset=offset,
        lang=lang,
        topics=topics,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max,
        sort=sort,
        order=order,
    )


@router.get("/export")
async def export_repos(
    params: RepoSearchParams = Depends(get_repo_search_params),
    svc: GitHubReposExportService = Depends(get_export_service),
) -> dict[str, str]:
    """
    Export GitHub repositories.

    Matching filters to a CSV file in the static directory.
    Query parameters are parsed into RepoSearchParams (including `topics`).
    """
    out: Path = await svc.export(params)
    return {"filename": out.name, "path": str(out)}
