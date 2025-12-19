import httpx
from typing import Dict, Any
from app.core.config import settings


class GitHubClient:
    def __init__(self):
        self.base_url = settings.GITHUB_API_URL
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    async def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 100,
        page: int = 1,
    ) -> Dict[str, Any]:
        """Поиск репозиториев через GitHub API"""
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/search/repositories",
                params=params,
                headers=self.headers,
            )

            response.raise_for_status()
            return response.json()
