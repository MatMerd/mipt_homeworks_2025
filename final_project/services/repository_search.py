from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from final_project.domain.repository import Repository
from final_project.infrastructure.csv_writer import (
    RepositoryCsvWriter,
    get_csv_writer
)
from final_project.infrastructure.github_client import (
    GitHubSearchClient,
    get_github_client,
)
from final_project.settings import settings
from final_project.web.api.github_repositories.schemas import SearchRepositoriesParams


@dataclass(frozen=True, slots=True)
class RepositorySearchService:
    """Search repositories in GitHub and export them into CSV."""

    client: GitHubSearchClient
    writer: RepositoryCsvWriter

    async def search_and_save(
        self, params: SearchRepositoriesParams
    ) -> tuple[Path, int]:
        """Search GitHub repositories and save them into `static/`."""
        filename = (
            f"repositories_{self._slug(params.lang)}_{params.limit}_{params.offset}.csv"
        )
        path = settings.static_dir / filename

        repositories = await self._search(params)
        written = await self.writer.write(path=path, repositories=repositories)
        return path, written

    async def _search(self, params: SearchRepositoriesParams) -> list[Repository]:
        per_page = 100
        page = params.offset // per_page + 1
        skip = params.offset % per_page

        query = self._build_query(params)
        collected: list[Repository] = []

        while len(collected) < params.limit:
            payload = await self.client.search_repositories_page(
                query=query, per_page=per_page, page=page
            )
            items = payload.get("items") or []
            if not items:
                break

            for item in items[skip:]:
                collected.append(Repository.from_github_item(item))
                if len(collected) >= params.limit:
                    break

            skip = 0
            page += 1

        return collected

    @staticmethod
    def _build_query(params: SearchRepositoriesParams) -> str:
        lang = f'"{params.lang}"' if " " in params.lang else params.lang

        stars = (
            f"stars:{params.stars_min}..{params.stars_max}"
            if params.stars_max is not None
            else f"stars:>={params.stars_min}"
        )
        forks = (
            f"forks:{params.forks_min}..{params.forks_max}"
            if params.forks_max is not None
            else f"forks:>={params.forks_min}"
        )
        license_filter = f"license:{params.license}" if params.license else ""

        query_parts = [f"language:{lang}", stars, forks]
        if license_filter:
            query_parts.append(license_filter)

        return " ".join(query_parts)

    @staticmethod
    def _slug(value: str) -> str:
        return value.strip().replace(" ", "_")


def get_repository_search_service(
    client: GitHubSearchClient = Depends(get_github_client),
    writer: RepositoryCsvWriter = Depends(get_csv_writer),
) -> RepositorySearchService:
    """Get repository search service with dependencies."""
    return RepositorySearchService(client=client, writer=writer)
