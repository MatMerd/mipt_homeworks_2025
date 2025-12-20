from typing import Any, cast

import httpx

from app.models import GitHubSearchParams, Repository


class GitHubClient:
    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url
        self.headers: dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    async def search_repositories(
        self,
        search_params: GitHubSearchParams,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/search/repositories"
        params: dict[str, str | int] = {
            "q": search_params.q,
            "sort": search_params.sort,
            "order": search_params.order,
            "per_page": search_params.per_page,
            "page": search_params.page,
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

    async def get_contributors_count(self, owner: str, repo: str) -> int:
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        params = {"per_page": 1, "anon": "true"}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params,
                headers=self.headers,
                timeout=30.0,
            )
            if response.status_code == 204:
                return 0
            response.raise_for_status()

            link_header = response.headers.get("Link", "")
            if 'rel="last"' in link_header:
                import re

                match = re.search(r'page=(\d+)>; rel="last"', link_header)
                if match:
                    return int(match.group(1))
            return len(response.json())

    async def fetch_all_repositories(
        self,
        query: str,
        limit: int,
        offset: int = 0,
        sort: str = "stars",
        order: str = "desc",
        contributors_min: int = 0,
        contributors_max: int | None = None,
    ) -> list[Repository]:
        repositories: list[Repository] = []
        per_page = min(100, limit + offset)
        page = 1
        total_fetched = 0
        skipped = 0

        while len(repositories) < limit:
            search_params = GitHubSearchParams(
                q=query,
                sort=sort,
                order=order,
                per_page=per_page,
                page=page,
            )
            data = await self.search_repositories(search_params)

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

                contributors_count: int | None = None
                if contributors_min > 0 or contributors_max is not None:
                    owner, repo_name = item["full_name"].split("/")
                    contributors_count = await self.get_contributors_count(owner, repo_name)

                    if contributors_count < contributors_min:
                        continue
                    if contributors_max is not None and contributors_count > contributors_max:
                        continue

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
                    contributors_count=contributors_count,
                )
                repositories.append(repo)

            if len(items) < per_page:
                break

            page += 1

            if data.get("total_count", 0) <= total_fetched:
                break

        return repositories
