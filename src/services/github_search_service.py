import csv
from pathlib import Path
from typing import Any

import aiofiles

from src.infrastructure.github_client import GitHubClient


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
        query_parts = [f"language:{lang}"]

        if stars_max is not None:
            query_parts.append(f"stars:{stars_min}..{stars_max}")
        else:
            query_parts.append(f"stars:>={stars_min}")

        if forks_max is not None:
            query_parts.append(f"forks:{forks_min}..{forks_max}")
        else:
            query_parts.append(f"forks:>={forks_min}")

        return " ".join(query_parts)

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

        all_repos: list[dict[str, Any]] = []
        total_needed = offset + limit
        per_page = min(100, total_needed)
        page = 1

        while len(all_repos) < total_needed:
            result = await self._client.search_repositories(
                query=query,
                sort="stars",
                order="desc",
                per_page=per_page,
                page=page,
            )

            items = result.get("items", [])
            if not items:
                break

            all_repos.extend(items)
            page += 1

            if len(items) < per_page:
                break

        repos_to_save = all_repos[offset : offset + limit]

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        filepath = self._static_dir / filename

        await self._save_to_csv(repos_to_save, filepath)

        return filepath

    async def _save_to_csv(
        self, repos: list[dict[str, Any]], filepath: Path
    ) -> None:
        self._static_dir.mkdir(parents=True, exist_ok=True)

        rows = []
        for repo in repos:
            rows.append({
                "name": repo.get("name", ""),
                "full_name": repo.get("full_name", ""),
                "description": repo.get("description", "") or "",
                "html_url": repo.get("html_url", ""),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", "") or "",
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
            })

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

        async with aiofiles.open(filepath, mode="w", newline="", encoding="utf-8") as f:
            output = []
            writer = csv.DictWriter(
                type("StringIO", (), {"write": lambda self, s: output.append(s)})(),
                fieldnames=fieldnames,
            )
            writer.writeheader()
            writer.writerows(rows)
            await f.write("".join(output))
