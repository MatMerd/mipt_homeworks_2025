from typing import Any

import httpx

from src.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubNotFoundError,
    GitHubRateLimitError,
    GitHubServerError,
)
from src.models import Repository


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str | None = None) -> None:
        self._token = token
        self._headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            self._headers["Authorization"] = f"Bearer {token}"

        self._client = httpx.AsyncClient(timeout=30.0)

    async def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 100,
        page: int = 1,
    ) -> dict[str, Any]:
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page,
        }

        try:
            response = await self._client.get(
                f"{self.BASE_URL}/search/repositories",
                headers=self._headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise GitHubRateLimitError() from e
            elif e.response.status_code == 404:
                raise GitHubNotFoundError() from e
            elif e.response.status_code == 401:
                raise GitHubAuthenticationError() from e
            elif e.response.status_code >= 500:
                raise GitHubServerError(f"GitHub server error: {e.response.status_code}") from e
            else:
                raise GitHubAPIError(
                    f"GitHub API error: {e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e
        except httpx.TimeoutException as e:
            raise GitHubAPIError("Request timeout", status_code=408) from e
        except httpx.RequestError as e:
            raise GitHubAPIError(f"Request failed: {str(e)}") from e

    async def search_repositories_as_models(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 100,
        page: int = 1,
    ) -> list[Repository]:
        response = await self.search_repositories(query, sort, order, per_page, page)

        items = response.get("items", [])
        repositories = []

        for idx, item in enumerate(items):
            position = (page - 1) * per_page + idx + 1
            repo = Repository.from_github_item(item, position)
            repositories.append(repo)

        return repositories

    async def close(self) -> None:
        await self._client.aclose()

