import os

from fastapi import APIRouter, Query
from typing import Any
from schemas import SearchParams
from services import RepositoryService
from infrastructure import GithubClient


router = APIRouter()

github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
repository_service = RepositoryService(github_client)


@router.get("/")
async def search_github_repositories(params: SearchParams = Query(...)) -> dict[str, Any]:
    response = await repository_service.execute_and_save(
        params
    )

    return response
