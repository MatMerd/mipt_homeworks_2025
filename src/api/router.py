from pathlib import Path

from fastapi import APIRouter, Depends, Query

from src.infrastructure.github_client import GitHubClient
from src.services.github_search_service import GitHubSearchService

router = APIRouter()

STATIC_DIR = Path(__file__).parent.parent.parent / "static"


def get_github_client() -> GitHubClient:
    return GitHubClient()


def get_search_service(
    client: GitHubClient = Depends(get_github_client),
) -> GitHubSearchService:
    return GitHubSearchService(github_client=client, static_dir=STATIC_DIR)


@router.get("/search")
async def search_repositories(
    limit: int = Query(..., gt=0, description="Number of repositories to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    lang: str = Query(..., description="Programming language"),
    stars_min: int = Query(0, ge=0, description="Minimum number of stars"),
    stars_max: int | None = Query(None, ge=0, description="Maximum number of stars"),
    forks_min: int = Query(0, ge=0, description="Minimum number of forks"),
    forks_max: int | None = Query(None, ge=0, description="Maximum number of forks"),
    service: GitHubSearchService = Depends(get_search_service),
) -> dict[str, str]:
    filepath = await service.search_and_save(
        limit=limit,
        offset=offset,
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max,
    )
    return {"message": "Repositories saved", "file": str(filepath)}
