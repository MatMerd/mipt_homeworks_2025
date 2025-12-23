import httpx
from dotenv import load_dotenv

from ..config import Settings
from ..schemas import SearchResponse

load_dotenv()


class GitHubClient:
    SEARCH_REPOS_ENDPOINT = "/search/repositories"

    def __init__(self, settings: Settings):
        self.base_url = settings.github_base_url
        self.token = settings.github_token
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 30,
        page: int = 1,
    ) -> SearchResponse:
        url = f"{self.base_url}{self.SEARCH_REPOS_ENDPOINT}"
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": min(per_page, 100),
            "page": page,
        }
        response = await self.client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        return SearchResponse(**data)

    async def close(self):
        await self.client.aclose()
