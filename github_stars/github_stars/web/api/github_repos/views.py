from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, Query, Request

from github_stars.services.github_repos.service import (
    GitHubReposExportService,
    RepoSearchParams,
)

SortField = Literal["stars", "forks", "updated"]
SortOrder = Literal["asc", "desc"]

router = APIRouter()


def get_export_service(request: Request) -> GitHubReposExportService:
    """Get GitHubReposExportService instance from the FastAPI application state."""
    return request.app.state.github_repos_export_service


@router.get("/export")
async def export_repos(
    limit: int = Query(..., ge=0),
    offset: int = Query(0, ge=0),
    lang: str = Query(..., min_length=1),
    stars_min: int = Query(0, ge=0),
    stars_max: int | None = Query(None, ge=0),
    forks_min: int = Query(0, ge=0),
    forks_max: int | None = Query(None, ge=0),
    svc: GitHubReposExportService = Depends(get_export_service),
    sort: SortField = Query("stars"),
    order: SortOrder = Query("desc"),
) -> dict[str, str]:
    """
    Export GitHub repositories.

    Matching filters to a CSV file in the static directory.
    """
    out: Path = await svc.export(
        RepoSearchParams(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
            sort=sort,
            order=order,
        )
    )
    return {"filename": out.name, "path": str(out)}
