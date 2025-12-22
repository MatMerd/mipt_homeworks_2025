from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Request

from github_stars.services.github_repos.service import (
    GitHubReposExportService,
    RepoSearchParams,
)

router = APIRouter()


def get_export_service(request: Request) -> GitHubReposExportService:
    """Get GitHubReposExportService instance from the FastAPI application state."""
    return request.app.state.github_repos_export_service


@router.get("/export")
async def export_repos(
    params: RepoSearchParams = Depends(),
    svc: GitHubReposExportService = Depends(get_export_service),
) -> dict[str, str]:
    """
    Export GitHub repositories.

    Matching filters to a CSV file in the static directory.
    Query parameters are parsed into RepoSearchParams (including `topics`).  # TOPICS FILTER CHANGE
    """
    out: Path = await svc.export(params)
    return {"filename": out.name, "path": str(out)}
