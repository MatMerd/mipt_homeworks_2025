from fastapi import Depends, Request

from final_project.final_project.infrastructure.github_client import GitHubClient
from final_project.final_project.services.repo_service import RepositoryService


def get_github_client(request: Request) -> GitHubClient:
    """Provide GitHub API client."""
    return request.app.state.github_client


def get_repository_service(
        client: GitHubClient = Depends(get_github_client),
) -> RepositoryService:
    """Provide repository service."""
    return RepositoryService(client=client, static_dir="static")
