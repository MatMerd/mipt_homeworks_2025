from pathlib import Path

from fastapi import FastAPI
from httpx import AsyncClient
from pytest import MonkeyPatch
from starlette import status


async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK


async def test_search_repositories_writes_csv(
    client: AsyncClient,
    fastapi_app: FastAPI,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Ensure the endpoint searches repositories and writes a CSV file."""
    from final_project.infrastructure.github_client import GitHubSearchClient
    from final_project.settings import settings

    fake_items = [
        {
            "name": "example",
            "description": "desc",
            "html_url": "https://github.com/example/example",
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-02T00:00:00Z",
            "homepage": None,
            "size": 1,
            "stargazers_count": 10,
            "forks_count": 2,
            "open_issues_count": 0,
            "watchers_count": 10,
            "language": "Python",
            "license": {"spdx_id": "MIT"},
            "topics": ["one", "two"],
            "has_issues": True,
            "has_projects": False,
            "has_downloads": True,
            "has_wiki": False,
            "has_pages": False,
            "has_discussions": False,
            "fork": False,
            "archived": False,
            "is_template": False,
            "default_branch": "main",
        }
    ]

    async def fake_search_page(
        self: GitHubSearchClient,
        *,
        query: str,
        per_page: int,
        page: int,
        sort: str = "stars",
        order: str = "desc",
    ) -> dict[str, object]:
        return {"items": fake_items}

    monkeypatch.setattr(
        GitHubSearchClient,
        "search_repositories_page",
        fake_search_page,
    )
    monkeypatch.setattr(settings, "static_dir", tmp_path)

    url = fastapi_app.url_path_for("search_repositories")
    response = await client.get(
        url,
        params={
            "limit": 1,
            "offset": 0,
            "lang": "Python",
            "stars_min": 0,
            "forks_min": 0,
        },
    )
    assert response.status_code == status.HTTP_200_OK

    expected_path = tmp_path / "repositories_Python_1_0.csv"
    assert expected_path.exists()
    assert expected_path.read_text(encoding="utf-8").startswith("Name,Description,URL,")


async def test_search_repositories_returns_422_for_invalid_ranges(
    client: AsyncClient,
    fastapi_app: FastAPI,
) -> None:
    """Ensure invalid min/max ranges are rejected by validation."""
    url = fastapi_app.url_path_for("search_repositories")
    response = await client.get(
        url,
        params={
            "limit": 1,
            "offset": 0,
            "lang": "Python",
            "stars_min": 10,
            "stars_max": 1,
            "forks_min": 0,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_search_repositories_propagates_github_error(
    client: AsyncClient,
    fastapi_app: FastAPI,
    monkeypatch: MonkeyPatch,
) -> None:
    """Ensure GitHub API error is returned to the client."""
    from final_project.infrastructure.github_client import (
        GitHubClientError,
        GitHubSearchClient,
    )

    async def fake_search_page_error(
        self: GitHubSearchClient,
        *,
        query: str,
        per_page: int,
        page: int,
        sort: str = "stars",
        order: str = "desc",
    ) -> dict[str, object]:
        raise GitHubClientError(status.HTTP_403_FORBIDDEN, "rate limit")

    monkeypatch.setattr(
        GitHubSearchClient,
        "search_repositories_page",
        fake_search_page_error,
    )

    url = fastapi_app.url_path_for("search_repositories")
    response = await client.get(
        url,
        params={
            "limit": 1,
            "offset": 0,
            "lang": "Python",
            "stars_min": 0,
            "forks_min": 0,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
