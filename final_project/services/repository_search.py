from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from final_project.domain.repository import Repository
from final_project.infrastructure.csv_writer import RepositoryCsvWriter
from final_project.infrastructure.github_client import GitHubSearchClient
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

        q = self._build_query(params)
        collected: list[Repository] = []

        while len(collected) < params.limit:
            payload = await self.client.search_repositories_page(
                q=q, per_page=per_page, page=page
            )
            items = payload.get("items") or []
            if not items:
                break

            for item in items[skip:]:
                collected.append(self._to_repository(item))
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
        return f"language:{lang} {stars} {forks}"

    @staticmethod
    def _to_repository(item: dict[str, Any]) -> Repository:
        license_info = item.get("license") or {}
        return Repository(
            name=str(item.get("name") or ""),
            description=item.get("description"),
            url=str(item.get("html_url") or ""),
            created_at=str(item.get("created_at") or ""),
            updated_at=str(item.get("updated_at") or ""),
            homepage=item.get("homepage") or None,
            size=int(item.get("size") or 0),
            stars=int(item.get("stargazers_count") or 0),
            forks=int(item.get("forks_count") or 0),
            issues=int(item.get("open_issues_count") or 0),
            watchers=int(item.get("watchers_count") or 0),
            language=item.get("language") or None,
            license=(license_info.get("spdx_id") or None),
            topics=Repository.coerce_topics(item.get("topics")),
            has_issues=bool(item.get("has_issues") or False),
            has_projects=bool(item.get("has_projects") or False),
            has_downloads=bool(item.get("has_downloads") or False),
            has_wiki=bool(item.get("has_wiki") or False),
            has_pages=bool(item.get("has_pages") or False),
            has_discussions=bool(item.get("has_discussions") or False),
            is_fork=bool(item.get("fork") or False),
            is_archived=bool(item.get("archived") or False),
            is_template=bool(item.get("is_template") or False),
            default_branch=str(item.get("default_branch") or ""),
        )

    @staticmethod
    def _slug(value: str) -> str:
        return value.strip().replace(" ", "_")


def build_repository_search_service() -> RepositorySearchService:
    """Create a service with default dependencies."""
    return RepositorySearchService(
        client=GitHubSearchClient(), writer=RepositoryCsvWriter()
    )
