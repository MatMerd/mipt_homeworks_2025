from typing import Any

import httpx


class GitHubClient:
    BASE_URL = "https://api.github.com/search/repositories"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=30.0,
        )

    async def search_repositories(
        self,
        query: str,
        per_page: int = 100,
        page: int = 1,
    ) -> dict[str, Any]:
        params = {
            "q": query,
            "per_page": per_page,
            "page": page,
            "sort": "stars",
            "order": "desc",
        }
        response = await self._client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()


github_client = GitHubClient()
