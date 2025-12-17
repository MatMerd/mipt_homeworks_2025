from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


class GitHubClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class GitHubSearchResponse:
    total_count: int
    items: list[dict[str, Any]]


class GitHubClient:
    def __init__(self, base_url: str = "https://api.github.com") -> None:
        self._base_url = base_url.rstrip("/")
        self._token = os.getenv("GITHUB_TOKEN")

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "mipt-homeworks-2025-homework-fastapi",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    async def search_repositories(
        self,
        *,
        q: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 100,
        page: int = 1,
    ) -> GitHubSearchResponse:
        url = f"{self._base_url}/search/repositories"
        params = {
            "q": q,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page,
        }

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
                resp = await client.get(url, params=params, headers=self._headers())  # type: ignore
        except httpx.HTTPError as exc:
            raise GitHubClientError(f"GitHub request failed: {exc}") from exc

        if resp.status_code >= 400:
            detail: str
            try:
                detail = resp.json().get("message", resp.text)
            except Exception:
                detail = resp.text
            raise GitHubClientError(f"GitHub API error {resp.status_code}: {detail}")
        data = resp.json()
        total_count = int(data.get("total_count", 0))
        items = data.get("items") or []
        if not isinstance(items, list):
            items = []
        return GitHubSearchResponse(total_count=total_count, items=items)
