import logging

from aiofile import async_open
from schemas import SearchParams, Repository
from infrastructure import GithubClient
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class RepositoryService:

    def __init__(self, github_client: GithubClient):
        self.github_client = github_client

    @staticmethod
    def build_github_query(params: SearchParams) -> str:
        query = [f"language:{params.lang}"]

        if params.stars_min > 0:
            query.append(f"stars:>={params.stars_min}")

        if params.stars_max is not None:
            query.append(f"stars:<={params.stars_max}")
        
        if params.forks_min > 0:
            query.append(f"forks:>={params.forks_min}")
        
        if params.forks_max is not None:
            query.append(f"forks:<={params.forks_max}")

        return ' '.join(query)
    
    async def execute_and_save(self, params: SearchParams) -> dict[str, Any]:
        query = self.build_github_query(params)
        logger.info(f"Поисковый запрос: {query}")

        try:
            repos = await self.github_client.search_repositories(
                query,
                params.limit,
                params.offset
            )
            logger.info(f"Найдено репозиториев: {len(repos)}")
        except Exception as e:
            logger.error(f"Ошибка при поиске репозиториев: {e}")

        filename = f"repositories_{params.lang}_{params.limit}_{params.offset}.csv"
        filepath = Path(__file__).parent.parent / "static" / filename

        logger.info(f"Сохранение в файл: {filename}")
        
        try:
            await self._save_repositories(repos, filepath)
            logger.info(f"Файл успешно сохранен: {filepath}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении файла {filename}: {e}")
            raise

        return {
            "file": filename,
            "count": len(repos)
        }

    async def _save_repositories(self, repositories: list[Repository], filepath: Path) -> None:
        lines = []
            
        lines.append(Repository.get_headers_csv())
            
        for repo in repositories:
            lines.append(repo.to_csv())
            
        async with async_open(filepath, "w", encoding="utf-8") as f:
            await f.write('\n'.join(lines))
