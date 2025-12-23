from typing import Any

from config import Settings
from infrastructure.github_client import GitHubClient
from repositories.exporter import CsvExporter
from schemas import SearchRepositoriesRequest, SearchResponse
from utils.timing import measure_time


class RepositoryService:
    def __init__(self, settings: Settings, exporter: CsvExporter = None):
        self.github_client = GitHubClient(settings)
        self.exporter = exporter or CsvExporter()

    def _build_search_query(
        self,
        lang: str | None = None,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> str:
        query_parts = []
        if lang:
            query_parts.append(f"language:{lang}")
        if stars_max is not None:
            query_parts.append(f"stars:{stars_min}..{stars_max}")
        else:
            query_parts.append(f"stars:>={stars_min}")
        if forks_max is not None:
            query_parts.append(f"forks:{forks_min}..{forks_max}")
        else:
            query_parts.append(f"forks:>={forks_min}")
        return " ".join(query_parts)

    @measure_time()
    async def search_repositories(
        self,
        limit: int,
        offset: int = 0,
        lang: str | None = None,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> list[dict[str, Any]]:
        query = self._build_search_query(lang, stars_min, stars_max, forks_min, forks_max)
        all_repos = []
        per_page = 100
        current_offset = offset
        while len(all_repos) < limit:
            page = current_offset // per_page + 1
            items_needed = min(limit - len(all_repos), per_page)
            result: SearchResponse = await self.github_client.search_repositories(
                query=query, sort="stars", order="desc", per_page=items_needed, page=page
            )
            repos = result.items
            if not repos:
                break
            start_idx = current_offset % per_page
            repos_slice = repos[start_idx:]
            all_repos.extend([repo.model_dump() for repo in repos_slice[: limit - len(all_repos)]])
            if len(repos) < items_needed:
                break
            current_offset += len(repos_slice)
        return all_repos

    @measure_time()
    async def search_and_export_to_csv(self, request: SearchRepositoriesRequest) -> tuple[str, int]:
        repositories = await self.search_repositories(**request.model_dump())
        lang_str = request.lang if request.lang else "all"
        filename = f"repositories_{lang_str}_{request.limit}_{request.offset}.csv"
        filepath = await self.exporter.export_to_csv(repositories, filename)
        return filepath, len(repositories)

    async def close(self):
        await self.github_client.close()
