from typing import Optional, Dict, Any
import httpx

class SearchManager:
    API_PATH = "https://api.github.com/search/repositories"

    def __init__(self, token: Optional[str] = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Search-Client/1.0"
        }

        if token:
            self.headers["Authorization"] = f"token {token}"

    def _build_range_filter(self, field: str, min_val: int, max_val: Optional[int]) -> str:
        """
        Создает фильтр диапазона для GitHub API

        Args:
            field: Поле для фильтрации (stars, forks)
            min_val: Минимальное значение
            max_val: Максимальное значение или None
        """
        if min_val > 0 and max_val is not None:
            return f"{field}:{min_val}..{max_val}"
        elif min_val > 0:
            return f"{field}:>={min_val}"
        elif max_val is not None:
            return f"{field}:<={max_val}"
        return ""

    def build_query(
            self,
            lang: Optional[str] = None,
            stars_min: int = 0,
            stars_max: Optional[int] = None,
            forks_min: int = 0,
            forks_max: Optional[int] = None,
            **kwargs
    ) -> str:
        query_parts = []

        # Основной текст запроса
        if "q" in kwargs and kwargs["q"]:
            query_parts.append(kwargs["q"])

        # Фильтр по языку
        if lang:
            query_parts.append(f"language:{lang}")
        elif "language" in kwargs and kwargs["language"]:
            query_parts.append(f"language:{kwargs['language']}")

        # Фильтр по звёздам
        stars_filter = self._build_range_filter("stars", stars_min, stars_max)
        if stars_filter:
            query_parts.append(stars_filter)
        elif "stars" in kwargs and kwargs["stars"]:
            query_parts.append(f"stars:{kwargs['stars']}")

        # Фильтр по форкам
        forks_filter = self._build_range_filter("forks", forks_min, forks_max)
        if forks_filter:
            query_parts.append(forks_filter)
        elif "forks" in kwargs and kwargs["forks"]:
            query_parts.append(f"forks:{kwargs['forks']}")

        # Фильтр по дате создания
        if "created" in kwargs and kwargs["created"]:
            query_parts.append(f"created:{kwargs['created']}")

        # Фильтр по дате последнего пуша
        if "pushed" in kwargs and kwargs["pushed"]:
            query_parts.append(f"pushed:{kwargs['pushed']}")

        # Фильтр по теме
        if "topic" in kwargs and kwargs["topic"]:
            query_parts.append(f"topic:{kwargs['topic']}")

        # Фильтр по лицензии
        if "license" in kwargs and kwargs["license"]:
            query_parts.append(f"license:{kwargs['license']}")

        # Архивные репозитории
        if "archived" in kwargs and kwargs["archived"]:
            query_parts.append("archived:true")
        elif "archived" in kwargs and not kwargs["archived"]:
            query_parts.append("archived:false")

        # Только форки
        if "fork" in kwargs and kwargs["fork"]:
            query_parts.append("fork:true")

        # Публичные/приватные
        if "is" in kwargs and kwargs["is"]:
            query_parts.append(f"is:{kwargs['is']}")

        # Фильтр по размеру
        if "size" in kwargs and kwargs["size"]:
            query_parts.append(f"size:{kwargs['size']}")

        return " ".join(query_parts)

    async def search(
            self,
            limit: int,
            offset: int,
            lang: Optional[str] = None,
            stars_min: int = 0,
            stars_max: Optional[int] = None,
            forks_min: int = 0,
            forks_max: Optional[int] = None,
            **additional_params) -> Dict[str, Any]:

        # Валидация параметров
        if limit <= 0 or limit > 100:
            limit = min(max(1, limit), 100)  # Ограничение GitHub: 100 на страницу

        if offset < 0:
            offset = 0

        # Преобразуем offset в page для GitHub API
        # GitHub API использует пагинацию по страницам
        page = (offset // limit) + 1

        # Строим поисковый запрос с новыми параметрами
        search_query = self.build_query(
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
            **additional_params
        )

        params = {
            "q": search_query,
            "sort": "stars",  # Сортировка по звездам по умолчанию
            "order": "desc",  # По убыванию по умолчанию
            "per_page": limit,
            "page": page
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                SearchManager.API_PATH,
                headers=self.headers,
                params=params
            )

            response.raise_for_status()
            return response.json()
