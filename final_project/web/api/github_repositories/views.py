from fastapi import APIRouter, Depends, HTTPException

from final_project.infrastructure.github_client import GitHubClientError
from final_project.services.repository_search import build_repository_search_service
from final_project.web.api.github_repositories.schemas import (
    SearchRepositoriesParams,
    SearchRepositoriesResponse,
)

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.get("/search", response_model=SearchRepositoriesResponse)
async def search_repositories(
    params: SearchRepositoriesParams = Depends(),
) -> SearchRepositoriesResponse:
    """Search GitHub repositories and save the result to CSV in `static/`."""
    service = build_repository_search_service()
    try:
        path, written = await service.search_and_save(params)
    except GitHubClientError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    return SearchRepositoriesResponse(csv_path=path, returned=written)
