from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from final_project.infrastructure.github_client import GitHubClientError
from final_project.services.repository_search import (
    RepositorySearchService,
    get_repository_search_service,
)
from final_project.web.api.github_repositories.schemas import (
    SearchRepositoriesParams,
    SearchRepositoriesResponse,
)

router = APIRouter(prefix="/repositories", tags=["repositories"])


def parse_search_params(
    limit: int = Query(..., gt=0),
    offset: int = Query(0, ge=0),
    lang: str = Query(..., min_length=1),
    stars_min: int = Query(0, ge=0),
    stars_max: int | None = Query(None, ge=0),
    forks_min: int = Query(0, ge=0),
    forks_max: int | None = Query(None, ge=0),
    license: str | None = Query(None, min_length=1),
) -> SearchRepositoriesParams:
    """Parse and validate query params into a single model instance."""
    try:
        return SearchRepositoriesParams(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
            license=license,
        )
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc


@router.get("/search", response_model=SearchRepositoriesResponse)
async def search_repositories(
    params: SearchRepositoriesParams = Depends(parse_search_params),
    service: RepositorySearchService = Depends(get_repository_search_service),
) -> SearchRepositoriesResponse:
    """Search GitHub repositories and save the result to CSV in `static/`."""
    try:
        search_result_path, written = await service.search_and_save(params)
    except GitHubClientError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    return SearchRepositoriesResponse(csv_path=search_result_path, returned=written)
