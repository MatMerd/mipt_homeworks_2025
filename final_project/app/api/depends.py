from typing import Annotated, Callable

from fastapi import Depends

from app.infrastructure.github_client import GitHubClient
from app.services.repository_service import RepositoryService
from app.settings import Settings


class Stub:
    def __init__(self, dependency: Callable, **kwargs: object) -> None:
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self) -> None:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Stub):
            return (
                self._dependency == other._dependency
                and self._kwargs == other._kwargs
            )
        if not self._kwargs:
            return self._dependency == other
        return False

    def __hash__(self) -> int:
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)


def get_settings() -> Settings:
    return Settings()


def get_github_client(
    settings: Annotated[Settings, Depends(Stub(Settings))],
) -> GitHubClient:
    return GitHubClient(
        base_url=settings.github_api_url,
        token=settings.github_token,
    )


def get_repository_service(
    client: Annotated[GitHubClient, Depends(Stub(GitHubClient))],
    settings: Annotated[Settings, Depends(Stub(Settings))],
) -> RepositoryService:
    return RepositoryService(
        client=client,
        static_dir=settings.static_dir,
    )
