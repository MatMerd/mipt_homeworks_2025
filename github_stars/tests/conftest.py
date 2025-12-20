from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest
from fakeredis import FakeRedis
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.asyncio import ConnectionPool

from github_stars.infrastructure.github_client import GitHubSearchResponse
from github_stars.services.github_repos.service import GitHubReposExportService
from github_stars.services.redis.dependency import get_redis_pool
from github_stars.web.application import get_app


class FakeGitHubClient:
    """Simple fake GitHub client for tests."""

    def __init__(self, items: list[dict[str, object]]) -> None:
        self._items = items
        self.calls: list[tuple[str, int, int, str, str]] = []

    async def search_repositories(
        self,
        *,
        q: str,
        page: int,
        per_page: int,
        sort: str = "stars",
        order: str = "desc",
    ) -> GitHubSearchResponse:
        """Return a paginated slice of fake repository items."""
        self.calls.append((q, page, per_page, sort, order))
        start = (page - 1) * per_page
        end = start + per_page
        return GitHubSearchResponse(
            total_count=len(self._items),
            incomplete_results=False,
            items=self._items[start:end],
        )


@pytest.fixture
def fake_github_items() -> list[dict[str, object]]:
    """Build a list of fake GitHub repository items for pagination and CSV tests."""
    items: list[dict[str, object]] = []
    for i in range(250):
        items.append(
            {
                "name": f"repo{i}",
                "description": "line1\nline2" if i == 0 else f"desc {i}",
                "html_url": f"https://github.com/org/repo{i}",
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": "2020-01-02T00:00:00Z",
                "homepage": "",
                "size": 123,
                "stargazers_count": 1000 - i,
                "forks_count": i,
                "open_issues_count": 7,
                "watchers_count": 42,
                "language": "Python",
                "license": {"spdx_id": "MIT"},
                "topics": ["a", "b"],
                "has_issues": True,
                "has_projects": True,
                "has_downloads": True,
                "has_wiki": False,
                "has_pages": False,
                "has_discussions": False,
                "fork": False,
                "archived": False,
                "is_template": False,
                "default_branch": "main",
            }
        )
    return items


@pytest.fixture
def fake_github_client(fake_github_items: list[dict[str, object]]) -> FakeGitHubClient:
    """Return a fake GitHub client serving a fixed list of repositories."""
    return FakeGitHubClient(fake_github_items)


@pytest.fixture
def github_repos_export_service(
    tmp_path: Path, fake_github_client: FakeGitHubClient
) -> GitHubReposExportService:
    """
    Create export service instance writing CSV.

    Files into a temporary static directory.
    """
    static_dir = tmp_path / "static"
    return GitHubReposExportService(github=fake_github_client, static_dir=static_dir)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeRedis()
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


@pytest.fixture
def fastapi_app(
    fake_redis_pool: ConnectionPool,
    github_repos_export_service: GitHubReposExportService,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    application.state.github_repos_export_service = github_repos_export_service
    return application


@pytest.fixture
async def client(
    fastapi_app: FastAPI, anyio_backend: Any
) -> AsyncGenerator[AsyncClient]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(
        transport=ASGITransport(fastapi_app), base_url="http://test", timeout=2.0
    ) as ac:
        yield ac
