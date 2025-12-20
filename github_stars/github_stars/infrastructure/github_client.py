from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class GitHubSearchResponse:
    """Parsed response from GitHub repository search endpoint."""

    total_count: int
    incomplete_results: bool
    items: list[dict[str, object]]


class GitHubClient:
    """HTTP client for GitHub Search API."""

    def __init__(self, http: httpx.AsyncClient, token: str | None = None) -> None:
        self._http = http
        self._token = token

    async def search_repositories(
        self,
        q: str,
        *,
        sort: str = "stars",
        order: str = "desc",
        page: int = 1,
        per_page: int = 100,
    ) -> GitHubSearchResponse:
        """
        Call GitHub.

        Search API.
        Return repositories for the given query and pagination.
        """
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        resp = await self._http.get(
            "https://api.github.com/search/repositories",
            params={
                "q": q,
                "sort": sort,
                "order": order,
                "page": page,
                "per_page": per_page,
            },
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()

        return GitHubSearchResponse(
            total_count=int(data.get("total_count", 0)),
            incomplete_results=bool(data.get("incomplete_results", False)),
            items=list(data.get("items", [])),
        )
