from typing import Any

import httpx


class SearchManager:
    """Клиент для GitHub Search API."""

    def __init__(
        self,
        api_url: str = "https://api.github.com/search/repositories",
        token: str | None = None,
    ) -> None:
        """
        Инициализирует клиент GitHub Search API.

        :param api_url: URL GitHub API (можно инжектировать для тестов)
        :param token: Токен GitHub для аутентификации (опционально)
        """
        self.api_url = api_url
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Search-Client/1.0",
        }

        if token:
            self.headers["Authorization"] = f"token {token}"

    async def search_repositories(
        self,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Выполняет поиск репозиториев через GitHub API.

        :param params: Параметры поиска (уже валидированные и подготовленные)
        :return: JSON ответ от GitHub API
        :raises RuntimeError: При ошибках API или сети
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    self.api_url,
                    headers=self.headers,
                    params=params,
                )
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    raise RuntimeError(
                        "GitHub API rate limit exceeded. Please try again later."
                    ) from None
                if e.response.status_code == 422:
                    query = params.get("q", "")
                    raise ValueError(f"Invalid search query: {query}") from None
                raise RuntimeError(
                    f"GitHub API error: {e.response.status_code} - {e.response.text}"
                ) from None
            except httpx.RequestError as e:
                raise RuntimeError(
                    f"Network error while calling GitHub API: {e!s}"
                ) from None
