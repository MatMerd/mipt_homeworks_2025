from typing import Any, cast

import httpx

from app.models import Repository
from app.settings import settings


class GitHubClient:
    def __init__(self) -> None:
        self.base_url = settings.github_api_url
        self.headers: dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if settings.github_token:
            self.headers["Authorization"] = f"Bearer {settings.github_token}"

    async def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 100,
        page: int = 1,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/search/repositories"
        params: dict[str, str | int] = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params,
                headers=self.headers,
                timeout=30.0,
            )
            response.raise_for_status()
            return cast(dict[str, Any], response.json())

    # Pagination
    async def fetch_all_repositories(
        self,
        query: str,
        limit: int,
        offset: int = 0,
        sort: str = "stars",
        order: str = "desc",
    ) -> list[Repository]:
        repositories: list[Repository] = []
        per_page = min(100, limit + offset)
        page = 1
        total_fetched = 0
        skipped = 0

        while len(repositories) < limit:
            data = await self.search_repositories(
                query=query,
                sort=sort,
                order=order,
                per_page=per_page,
                page=page,
            )

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                total_fetched += 1

                if skipped < offset:
                    skipped += 1
                    continue

                if len(repositories) >= limit:
                    break

                repo = Repository(
                    name=item["name"],
                    full_name=item["full_name"],
                    html_url=item["html_url"],
                    description=item.get("description"),
                    language=item.get("language"),
                    stargazers_count=item["stargazers_count"],
                    forks_count=item["forks_count"],
                    watchers_count=item["watchers_count"],
                    open_issues_count=item["open_issues_count"],
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                )
                repositories.append(repo)

            if len(items) < per_page:
                break

            page += 1

            if data.get("total_count", 0) <= total_fetched:
                break

        return repositories


github_client = GitHubClient()
