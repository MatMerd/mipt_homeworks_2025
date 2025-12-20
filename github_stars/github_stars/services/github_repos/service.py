from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Literal, Protocol

import aiofiles
from pydantic import BaseModel, model_validator

from github_stars.infrastructure.github_client import GitHubSearchResponse

SortField = Literal["stars", "forks", "updated"]
SortOrder = Literal["asc", "desc"]


class GitHubSearchClient(Protocol):
    """Protocol for GitHub search clients used by the export service."""

    async def search_repositories(
        self,
        *,
        q: str,
        page: int,
        per_page: int,
        sort: str = "stars",
        order: str = "desc",
    ) -> GitHubSearchResponse:
        """Search repositories using GitHub Search API and return a parsed response."""
        ...


class RepoSearchParams(BaseModel):
    """Parameters for GitHub repository search and CSV export."""

    limit: int
    offset: int
    lang: str

    stars_min: int = 0
    stars_max: int | None = None
    forks_min: int = 0
    forks_max: int | None = None

    sort: SortField = "stars"
    order: SortOrder = "desc"

    @model_validator(mode="after")
    def _validate_ranges(self) -> RepoSearchParams:
        if self.stars_max is not None and self.stars_min > self.stars_max:
            raise ValueError("stars_min must be <= stars_max")
        if self.forks_max is not None and self.forks_min > self.forks_max:
            raise ValueError("forks_min must be <= forks_max")
        return self


class GitHubReposExportService:
    """Service that exports GitHub repositories matching filters into a CSV file."""

    def __init__(self, github: GitHubSearchClient, static_dir: Path) -> None:
        self._github = github
        self._static_dir = static_dir

    def _build_q(self, p: RepoSearchParams) -> str:
        parts: list[str] = []
        parts.append(f"language:{p.lang}")

        if p.stars_max is None:
            parts.append(f"stars:>={p.stars_min}")
        else:
            parts.append(f"stars:{p.stars_min}..{p.stars_max}")

        if p.forks_max is None:
            parts.append(f"forks:>={p.forks_min}")
        else:
            parts.append(f"forks:{p.forks_min}..{p.forks_max}")

        return " ".join(parts)

    async def export(self, p: RepoSearchParams) -> Path:
        """
        Fetch repositories from GitHub.

        Search API and write them to a CSV file in the static directory.
        """
        limit = max(0, p.limit)
        offset = max(0, p.offset)
        self._static_dir.mkdir(parents=True, exist_ok=True)
        out = self._static_dir / f"repositories_{p.lang}_{limit}_{offset}.csv"
        if limit == 0:
            await self._write_csv(out, [])
            return out
        max_window = 1000
        end = min(offset + limit, max_window)
        need = max(0, end - offset)
        if need == 0:
            await self._write_csv(out, [])
            return out
        q = self._build_q(p)
        per_page = 100
        first_page = offset // per_page + 1
        last_page = (end - 1) // per_page + 1
        all_items: list[dict[str, object]] = []
        for page in range(first_page, last_page + 1):
            resp = await self._github.search_repositories(
                q=q,
                page=page,
                per_page=per_page,
                sort=p.sort,
                order=p.order,
            )
            all_items.extend(resp.items)

        start = offset - (first_page - 1) * per_page
        sliced = all_items[start : start + need]

        await self._write_csv(out, sliced)
        return out

    async def _write_csv(self, path: Path, items: list[dict[str, object]]) -> None:
        columns = [
            "Name",
            "Description",
            "URL",
            "Created At",
            "Updated At",
            "Homepage",
            "Size",
            "Stars",
            "Forks",
            "Issues",
            "Watchers",
            "Language",
            "License",
            "Topics",
            "Has Issues",
            "Has Projects",
            "Has Downloads",
            "Has Wiki",
            "Has Pages",
            "Has Discussions",
            "Is Fork",
            "Is Archived",
            "Is Template",
            "Default Branch",
        ]

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=columns)
        writer.writeheader()

        for r in items:
            license_obj = r.get("license") or {}
            license_spdx = ""
            if isinstance(license_obj, dict):
                spdx = license_obj.get("spdx_id")
                license_spdx = spdx if isinstance(spdx, str) else ""

            topics = r.get("topics") or []
            topics_str = str(topics)

            desc = r.get("description")
            all_desc = desc if isinstance(desc, str) else ""

            writer.writerow(
                {
                    "Name": r.get("name") or "",
                    "Description": (all_desc.replace("\n", " ").strip())
                    .replace("\n", " ")
                    .strip(),
                    "URL": r.get("html_url") or "",
                    "Created At": r.get("created_at") or "",
                    "Updated At": r.get("updated_at") or "",
                    "Homepage": r.get("homepage") or "",
                    "Size": r.get("size") or 0,
                    "Stars": r.get("stargazers_count") or 0,
                    "Forks": r.get("forks_count") or 0,
                    "Issues": r.get("open_issues_count") or 0,
                    "Watchers": r.get("watchers_count") or 0,
                    "Language": r.get("language") or "",
                    "License": license_spdx,
                    "Topics": topics_str,
                    "Has Issues": bool(r.get("has_issues")),
                    "Has Projects": bool(r.get("has_projects")),
                    "Has Downloads": bool(r.get("has_downloads")),
                    "Has Wiki": bool(r.get("has_wiki")),
                    "Has Pages": bool(r.get("has_pages")),
                    "Has Discussions": bool(r.get("has_discussions")),
                    "Is Fork": bool(r.get("fork")),
                    "Is Archived": bool(r.get("archived")),
                    "Is Template": bool(r.get("is_template")),
                    "Default Branch": r.get("default_branch") or "",
                }
            )

        async with aiofiles.open(path, "w", encoding="utf-8", newline="") as f:
            await f.write(buf.getvalue())
