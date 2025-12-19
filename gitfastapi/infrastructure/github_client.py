import httpx
from typing import Any, Optional

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        self.client = httpx.AsyncClient(headers=headers, timeout=30.0)

    async def search_repositories(
            self,
            query: str,
            sort: str = "stars",
            order: str = "desc",
            page: int = 1,
            per_page: int = 100
    ) -> dict[str, Any]:
        params: dict[str, str | int] = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page,
        }
        response = await self.client.get(GITHUB_SEARCH_URL, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
