from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from final_project.settings import settings


class GitHubClientError(RuntimeError):
    """GitHub API request failed."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


@dataclass(frozen=True, slots=True)
class GitHubSearchClient:
    """Minimal async client for GitHub `search/repositories`."""

    async def search_repositories_page(
        self,
        *,
        q: str,
        per_page: int,
        page: int,
        sort: str = "stars",
        order: str = "desc",
    ) -> dict[str, Any]:
        """Request one search page from GitHub."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "final_project",
        }
        if settings.github_token:
            headers["Authorization"] = f"Bearer {settings.github_token}"

        params: dict[str, str | int] = {
            "q": q,
            "per_page": per_page,
            "page": page,
            "sort": sort,
            "order": order,
        }

        async with httpx.AsyncClient(
            timeout=30.0,
            headers=headers,
            base_url=str(settings.github_base_url),
        ) as client:
            response = await client.get("/search/repositories", params=params)

        if response.is_error:
            raise GitHubClientError(response.status_code, response.text)

        return response.json()
