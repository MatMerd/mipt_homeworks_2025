from github_repo_api.infrastructure.search_manager import SearchManager
from github_repo_api.services.csv_converter import CSVConverter
from github_repo_api.services.query_builder import GitHubQueryBuilder


class RepositoryService:
    """Сервис для обработки операций поиска репозиториев."""

    def __init__(
        self,
        search_manager: SearchManager | None = None,
        query_builder: GitHubQueryBuilder | None = None,
    ) -> None:
        """
        Инициализирует сервис.

        :param search_manager: Клиент для GitHub API
        :param query_builder: Билдер поисковых запросов
        """
        self.search_manager = search_manager or SearchManager()
        self.query_builder = query_builder or GitHubQueryBuilder()

    async def search_and_save_repositories(
        self,
        limit: int,
        offset: int,
        lang: str | None = None,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> str:
        """
        Ищет репозитории и сохраняет их в CSV файл.

        :param limit: Количество репозиториев для поиска
        :param offset: Смещение для пагинации
        :param lang: Язык программирования
        :param stars_min: Минимальное количество звезд
        :param stars_max: Максимальное количество звезд
        :param forks_min: Минимальное количество форков
        :param forks_max: Максимальное количество форков
        :return: Имя CSV файла
        """
        self.query_builder.validate_search_params(
            limit=limit,
            offset=offset,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )

        search_query = self.query_builder.build_search_query(
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )

        search_params = self.query_builder.prepare_search_params(
            query=search_query,
            limit=limit,
            offset=offset,
        )

        github_data = await self.search_manager.search_repositories(
            params=search_params
        )

        csv_converter = CSVConverter(github_data)

        lang_part = lang if lang else "all"
        csv_filename = f"repositories_{lang_part}_{limit}_{offset}.csv"

        csv_converter.save_csv(csv_filename)

        return csv_filename
