from typing import Any

import httpx


class GitHubClient:
    API_ROOT = "https://api.github.com"

    def __init__(self, token: str | None = None) -> None:
        self._build_and_assign_client(token)

    def _build_and_assign_client(self, token: str | None) -> None:
        auth_header = {"Authorization": f"Bearer {token}"} if token else {}
        request_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **auth_header,
        }

        self._client = httpx.AsyncClient(
            base_url=self.API_ROOT.strip(),
            headers=request_headers,
            timeout=httpx.Timeout(30.0),
        )

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
            "per_page": min(per_page, 100),
            "page": max(page, 1),
        }

        raw_response = await self._client.request(
            "GET", "/search/repositories", params=params
        )
        raw_response.raise_for_status()
        payload = raw_response.json()

        return payload

    async def close(self) -> None:
        if hasattr(self, "_client") and self._client.is_closed is False:
            await self._client.aclose()
