import csv
import io
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import aiofiles

from src.other.github_client import GitHubClient


class GitHubSearchService:
    def __init__(self, github_client: GitHubClient, static_dir: Path) -> None:
        self._client = github_client
        self._static_dir = static_dir

    def _build_query(
        self,
        lang: str,
        stars_min: int,
        stars_max: int | None,
        forks_min: int,
        forks_max: int | None,
    ) -> str:
        parts = [f"language:{lang}"]

        stars_clause = (
            f"stars:{stars_min}..{stars_max}"
            if stars_max is not None
            else f"stars:>={stars_min}"
        )
        forks_clause = (
            f"forks:{forks_min}..{forks_max}"
            if forks_max is not None
            else f"forks:>={forks_min}"
        )

        parts.extend([stars_clause, forks_clause])
        return " ".join(parts)

    async def search_and_save(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> Path:
        query = self._build_query(lang, stars_min, stars_max, forks_min, forks_max)
        required_total = offset + limit

        async def fetch_pages() -> AsyncGenerator[dict[str, Any], None]:
            page_num = 1
            per_request = min(100, required_total)
            fetched = 0

            while fetched < required_total:
                response = await self._client.search_repositories(
                    query=query,
                    sort="stars",
                    order="desc",
                    per_page=per_request,
                    page=page_num,
                )
                items = response.get("items", [])
                if not items:
                    break

                for item in items:
                    yield item
                    fetched += 1
                    if fetched >= required_total:
                        return

                if len(items) < per_request:
                    break
                page_num += 1

        all_items = []
        async for repo in fetch_pages():
            all_items.append(repo)
        slice_to_save = all_items[offset : offset + limit]

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        filepath = self._static_dir / filename
        await self._save_to_csv(slice_to_save, filepath)
        return filepath

    async def _save_to_csv(self, repos: list[dict[str, Any]], filepath: Path) -> None:
        self._static_dir.mkdir(parents=True, exist_ok=True)

        buffer = io.StringIO()
        fieldnames = [
            "name",
            "full_name",
            "description",
            "html_url",
            "stars",
            "forks",
            "language",
            "created_at",
            "updated_at",
        ]

        writer = csv.DictWriter(
            buffer, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()

        for repo in repos:
            writer.writerow(
                {
                    "name": repo.get("name", ""),
                    "full_name": repo.get("full_name", ""),
                    "description": repo.get("description") or "",
                    "html_url": repo.get("html_url", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "language": repo.get("language") or "",
                    "created_at": repo.get("created_at", ""),
                    "updated_at": repo.get("updated_at", ""),
                }
            )

        async with aiofiles.open(
            filepath, mode="w", encoding="utf-8", newline=""
        ) as afp:
            await afp.write(buffer.getvalue())
