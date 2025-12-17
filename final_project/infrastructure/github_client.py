import httpx
import asyncio
import logging

from typing import Optional
from schemas import Repository


logger = logging.getLogger(__name__)


class GithubClient:
    def __init__(self, github_token: Optional[str] = None) -> None:
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        if github_token:
            self.headers["Authorization"] = f"Bearer {github_token}"
        else:
            logger.warning("GitHub Personal Access Token не указан.")

    async def search_repositories(self, query: str, limit: int, offset: int) -> list[Repository]:
        total = limit + offset
        all_repos: list[Repository] = []

        MAX_PARALLEL = 3

        pages = (total + 99) // 100
        page = 1

        async with httpx.AsyncClient(timeout=30.0, headers=self.headers) as client:
            while len(all_repos) < total and page <= pages:
                pages_per_batch = min(
                    MAX_PARALLEL,
                    pages - page + 1
                )

                tasks = []
                for i in range(pages_per_batch):
                    cur_page = page + i
                    task = self._fetch_page(client, query, cur_page)
                    tasks.append(task)

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for i, result in enumerate(results):
                    if isinstance(result, BaseException):
                        logger.error(f"Ошибка при загрузке страницы {page + i}: {result}")
                        continue

                    all_repos.extend(result)

                    if len(result) < 100:
                        return all_repos[offset:offset + limit]
                    
                page += pages_per_batch

        return all_repos[offset:offset + limit]
    
    async def _fetch_page(self, client: httpx.AsyncClient, query: str, page: int) -> list[Repository]:
        params: dict[str, str | int] = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }
            
        url = f"{self.base_url}/search/repositories"

        resp = await client.get(
            url,
            params=params
        )
        resp.raise_for_status()
        data = resp.json()
        return [Repository(**item) for item in data["items"]]
