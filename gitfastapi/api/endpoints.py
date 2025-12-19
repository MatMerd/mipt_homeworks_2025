from fastapi import APIRouter, Query, Depends
from typing import Optional
from gitfastapi.services.repository_service import RepositoryService
from gitfastapi.infrastructure.github_client import GitHubClient

router = APIRouter()

async def get_github_client():
    client = GitHubClient()
    try:
        yield client
    finally:
        await client.close()

def get_repository_service(client: GitHubClient = Depends(get_github_client)):
    return RepositoryService(client)

@router.get("/repos/save")
async def save_repositories(
    limit: int = Query(..., gt=0),
    offset: int = Query(0, ge=0),
    lang: str = Query(..., alias="lang"),
    stars_min: int = 0,
    stars_max: Optional[int] = None,
    forks_min: int = 0,
    forks_max: Optional[int] = None,
    service: RepositoryService = Depends(get_repository_service),
):
    return await service.search_and_save_repositories(
        limit=limit,
        offset=offset,
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max
    )
