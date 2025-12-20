from typing import Any, ClassVar

import httpx


class SearchManager:
    """
    Класс обертка над GitHub API.

    Получает на вход аргументы и возвращает json файл.
    """

    API_PATH = "https://api.github.com/search/repositories"
    REPO_STUFF: ClassVar[list[str]] = [
        "created",
        "pushed",
        "topic",
        "license",
        "archived",
        "fork",
        "is",
        "size",
    ]

    def __init__(self, token: str | None = None) -> None:
        """:param token: Токен для гитхаба (влияет на получаемую информацию)"""
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Search-Client/1.0",
        }

        if token:
            self.headers["Authorization"] = f"token {token}"

    def _build_range_filter(self, field: str, min_val: int, max_val: int | None) -> str:
        """
        Создает фильтр диапазона для GitHub API.

        Args:
            field: Поле для фильтрации (stars, forks)
            min_val: Минимальное значение
            max_val: Максимальное значение или None
        """
        if min_val > 0 and max_val is not None:
            return f"{field}:{min_val}..{max_val}"
        if min_val > 0:
            return f"{field}:>={min_val}"
        if max_val is not None:
            return f"{field}:<={max_val}"
        return ""

    def build_query(
        self,
        lang: str | None = None,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Обрабатывает аргументы и возвращает строку запрос для GitHub API.

        :param lang: Язык репозитория
        :param stars_min: Минимальные звезды
        :param stars_max: Максимальные звезды
        :param forks_min: Минимальные форки
        :param forks_max: Максимальные форки
        :param kwargs:
        :return: Строка-запрос для GitHub API
        """
        query_parts = []

        # Основной текст запроса
        if kwargs.get("q"):
            query_parts.append(kwargs["q"])

        # Фильтр по языку
        if lang:
            query_parts.append(f"language:{lang}")
        elif kwargs.get("language"):
            query_parts.append(f"language:{kwargs['language']}")

        # Фильтр по звёздам
        stars_filter = self._build_range_filter("stars", stars_min, stars_max)
        if stars_filter:
            query_parts.append(stars_filter)
        elif kwargs.get("stars"):
            query_parts.append(f"stars:{kwargs['stars']}")

        # Фильтр по форкам
        forks_filter = self._build_range_filter("forks", forks_min, forks_max)
        if forks_filter:
            query_parts.append(forks_filter)
        elif kwargs.get("forks"):
            query_parts.append(f"forks:{kwargs['forks']}")

        for param in SearchManager.REPO_STUFF:
            if kwargs.get(param):
                query_parts.append(f"{param}:{kwargs[param]}")

        return " ".join(query_parts)

    async def search(
        self,
        limit: int,
        offset: int,
        lang: str | None = None,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
        **additional_params: Any,
    ) -> dict[str, Any]:
        """
        Получает параметры извне и выдает json ответ от GitHub API.

        :param limit: число реп в ответе (не более 100)
        :param offset: сдвиг, если реп больше чем limit
        :param lang: язык репозитория
        :param stars_min: минимальное число звезд
        :param stars_max: максимальное число звезд
        :param forks_min: минимальное число форков
        :param forks_max: максимальное число форков
        :param additional_params:

        :return: json ответ GitHub API
        """

        # Валидация параметров
        if limit <= 0 or limit > 100:
            limit = min(max(1, limit), 100)  # Ограничение GitHub: 100 на страницу

        offset = max(offset, 0)

        page = (offset // limit) + 1

        search_query = self.build_query(
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
            **additional_params,
        )

        params: dict[str, Any] = {
            "q": search_query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit,
            "page": page,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                SearchManager.API_PATH, headers=self.headers, params=params
            )

            response.raise_for_status()
            return response.json()
