from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from final_project.settings import settings


@dataclass
class GitHubClientError(RuntimeError):
    """GitHub API request failed."""

    status_code: int
    detail: str


class GitHubSearchClient:
    """Async client for GitHub `search/repositories`."""

    __slots__ = ("_client",)

    def __init__(self) -> None:
        """Initialize GitHub client with reusable HTTP client."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "final_project",
        }
        if settings.github_token:
            headers["Authorization"] = f"Bearer {settings.github_token}"

        self._client = httpx.AsyncClient(
            timeout=30.0,
            headers=headers,
            base_url=str(settings.github_base_url),
        )

    async def search_repositories_page(
        self,
        *,
        query: str,
        per_page: int,
        page: int,
        sort: str = "stars",
        order: str = "desc",
    ) -> dict[str, Any]:
        """Request one search page from GitHub."""
        params: dict[str, str | int] = {
            "q": query,
            "per_page": per_page,
            "page": page,
            "sort": sort,
            "order": order,
        }

        response = await self._client.get("/search/repositories", params=params)

        if response.is_error:
            raise GitHubClientError(response.status_code, response.text)

        return response.json()

    async def aclose(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()


def get_github_client() -> GitHubSearchClient:
    """Get singleton GitHub client instance."""
    return GitHubSearchClient()
