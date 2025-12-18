from fastapi import Depends
import os
from homework_final.infrastructure.github_client import GitHubClient
from homework_final.services.repo_service import RepositoryService


def get_github_base_url() -> str:
    return os.getenv("GITHUB_BASE_URL", "https://api.github.com/search/repositories")


def get_github_client(base_url: str = Depends(get_github_base_url)) -> GitHubClient:
    return GitHubClient(base_url=base_url)


def get_repository_service(
        client: GitHubClient = Depends(get_github_client),
) -> RepositoryService:
    return RepositoryService(client=client)
