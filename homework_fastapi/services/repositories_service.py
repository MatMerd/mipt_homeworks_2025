from __future__ import annotations

from pathlib import Path
from typing import Any

from homework_fastapi.services.csv_writer import write_repositories_csv
from homework_fastapi.services.pagination import PaginationPlan, plan_pagination
from homework_fastapi.services.query_builder import build_github_query
from homework_fastapi.services.repository_mapper import repo_to_csv_row, safe_slug
from homework_fastapi.web.infrastructure.github_client import GitHubClient


class RepositoriesService:
    def __init__(self, client: GitHubClient | None = None) -> None:
        self._client = client or GitHubClient()

    async def search_and_save_csv(
        self,
        *,
        lang: str,
        limit: int,
        offset: int,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> dict[str, object]:
        q = build_github_query(
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )

        plan = plan_pagination(limit=limit, offset=offset, per_page=100)
        items = await self._fetch_items(q=q, plan=plan)
        sliced = items[plan.start_index : plan.start_index + limit]

        static_dir = Path(__file__).resolve().parent.parent / "static"
        file_name = f"repositories_{safe_slug(lang)}_{limit}_{offset}.csv"
        out_path = static_dir / file_name

        await write_repositories_csv(out_path, (repo_to_csv_row(r) for r in sliced))
        return {
            "query": q,
            "count": len(sliced),
            "file_name": file_name,
            "file_path": str(out_path),
        }

    async def _fetch_items(
        self, *, q: str, plan: PaginationPlan
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        page = plan.start_page
        while len(items) < plan.need_total:
            resp = await self._client.search_repositories(
                q=q,
                sort="stars",
                order="desc",
                per_page=plan.per_page,
                page=page,
            )
            items.extend(resp.items)
            if len(resp.items) < plan.per_page:
                break
            page += 1
            if page > 10:
                break
        return items
