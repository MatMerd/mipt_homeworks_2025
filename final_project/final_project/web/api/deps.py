from fastapi import Depends

from final_project.final_project.infrastructure.github_client import GitHubClient
from final_project.final_project.services.repo_service import RepositoryService
from final_project.final_project.settings import Settings


def get_settings() -> Settings:
    """Provide application settings."""
    return Settings()


def get_github_client(settings: Settings = Depends(get_settings)) -> GitHubClient:
    """Provide GitHub API client."""
    return GitHubClient(
        base_url=settings.GITHUB_BASE_URL,
        api_base_url=settings.GITHUB_API_BASE_URL,
        token=settings.GITHUB_TOKEN,
    )


def get_repository_service(
    client: GitHubClient = Depends(get_github_client),
) -> RepositoryService:
    """Provide repository service."""
    return RepositoryService(client=client, static_dir="static")
