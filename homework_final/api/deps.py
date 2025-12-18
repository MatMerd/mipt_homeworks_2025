from fastapi import Depends
from homework_final.infrastructure.github_client import GitHubClient
from homework_final.services.repo_service import RepositoryService


def get_github_client() -> GitHubClient:
    return GitHubClient()


def get_repository_service(
        client: GitHubClient = Depends(get_github_client),
) -> RepositoryService:
    return RepositoryService(client=client)
