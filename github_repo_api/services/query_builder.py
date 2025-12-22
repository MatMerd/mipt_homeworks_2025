from typing import Any


class GitHubQueryBuilder:
    """Класс для построения поисковых запросов GitHub API."""

    @staticmethod
    def validate_search_params(
        limit: int,
        offset: int,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> None:
        """
        Валидирует параметры поиска.

        :param limit: Количество результатов на страницу
        :param offset: Смещение для пагинации
        :param stars_min: Минимальное количество звезд
        :param stars_max: Максимальное количество звезд
        :param forks_min: Минимальное количество форков
        :param forks_max: Максимальное количество форков
        :raises ValueError: Если параметры невалидны
        """
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        if offset < 0:
            raise ValueError("offset must be non-negative")

        if stars_max is not None and stars_min > stars_max:
            raise ValueError("stars_min cannot be greater than stars_max")

        if forks_max is not None and forks_min > forks_max:
            raise ValueError("forks_min cannot be greater than forks_max")

    @staticmethod
    def build_search_query(
        lang: str | None = None,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> str:
        """
        Строит поисковый запрос для GitHub API.

        :param lang: Язык программирования
        :param stars_min: Минимальное количество звезд
        :param stars_max: Максимальное количество звезд
        :param forks_min: Минимальное количество форков
        :param forks_max: Максимальное количество форков
        :return: Поисковый запрос
        """
        query_parts = []

        if lang:
            query_parts.append(f"language:{lang}")

        if stars_min > 0 and stars_max is not None:
            query_parts.append(f"stars:{stars_min}..{stars_max}")
        elif stars_min > 0:
            query_parts.append(f"stars:>={stars_min}")
        elif stars_max is not None:
            query_parts.append(f"stars:<={stars_max}")

        if forks_min > 0 and forks_max is not None:
            query_parts.append(f"forks:{forks_min}..{forks_max}")
        elif forks_min > 0:
            query_parts.append(f"forks:>={forks_min}")
        elif forks_max is not None:
            query_parts.append(f"forks:<={forks_max}")

        return " ".join(query_parts) if query_parts else "stars:>0"

    @staticmethod
    def calculate_page_number(offset: int, limit: int) -> int:
        """
        Вычисляет номер страницы для GitHub API.

        :param offset: Смещение
        :param limit: Количество результатов на страницу
        :return: Номер страницы (начиная c 1)
        """
        return (offset // limit) + 1

    @staticmethod
    def prepare_search_params(
        query: str,
        limit: int = 30,
        offset: int = 0,
        sort: str = "stars",
        order: str = "desc",
    ) -> dict[str, Any]:
        """
        Подготавливает параметры для HTTP запроса.

        :param query: Поисковый запрос
        :param limit: Количество результатов на страницу
        :param offset: Смещение для пагинации
        :param sort: Поле сортировки
        :param order: Порядок сортировки
        :return: Словарь параметров для HTTP запроса
        """
        page = GitHubQueryBuilder.calculate_page_number(offset, limit)

        return {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": limit,
            "page": page,
        }
