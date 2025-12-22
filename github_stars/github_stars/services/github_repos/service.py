from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Literal, Protocol, Any, Sequence

import aiofiles
from pydantic import BaseModel, Field, ConfigDict, model_validator

from github_stars.infrastructure.github_client import GitHubSearchResponse


SortField = Literal["stars", "forks", "updated"]
SortOrder = Literal["asc", "desc"]


class RepoSearchParams(BaseModel):
    """
    Parameters for GitHub repository search and CSV export.
    Used as a dependency in FastAPI views to parse Query parameters automatically.
    """

    limit: int = Field(..., ge=0, description="Max records to export")
    offset: int = Field(0, ge=0, description="Pagination offset")
    lang: str = Field(..., min_length=1, description="Programming language")

    topics: list[str] = Field(
        default_factory=list,
        description="Repository topics. Repeat query parameter: topics=python&topics=fastapi",
    )

    stars_min: int = Field(0, ge=0)
    stars_max: int | None = Field(None, ge=0)
    forks_min: int = Field(0, ge=0)
    forks_max: int | None = Field(None, ge=0)

    sort: SortField = "stars"
    order: SortOrder = "desc"

    @model_validator(mode="after")
    def _validate_ranges(self) -> "RepoSearchParams":
        if self.stars_max is not None and self.stars_min > self.stars_max:
            raise ValueError("stars_min must be <= stars_max")
        if self.forks_max is not None and self.forks_min > self.forks_max:
            raise ValueError("forks_min must be <= forks_max")
        return self


class RepoReportItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., alias="Name")
    description: str = Field(default="", alias="Description")
    url: str = Field(..., alias="URL")
    created_at: str = Field(..., alias="Created At")
    updated_at: str = Field(..., alias="Updated At")
    homepage: str = Field(default="", alias="Homepage")
    size: int = Field(default=0, alias="Size")
    stars: int = Field(default=0, alias="Stars")
    forks: int = Field(default=0, alias="Forks")
    issues: int = Field(default=0, alias="Issues")
    watchers: int = Field(default=0, alias="Watchers")
    language: str = Field(default="", alias="Language")
    license: str = Field(default="", alias="License")
    topics: str = Field(default="[]", alias="Topics")

    has_issues: bool = Field(default=False, alias="Has Issues")
    has_projects: bool = Field(default=False, alias="Has Projects")
    has_downloads: bool = Field(default=False, alias="Has Downloads")
    has_wiki: bool = Field(default=False, alias="Has Wiki")
    has_pages: bool = Field(default=False, alias="Has Pages")
    has_discussions: bool = Field(default=False, alias="Has Discussions")
    is_fork: bool = Field(default=False, alias="Is Fork")
    is_archived: bool = Field(default=False, alias="Is Archived")
    is_template: bool = Field(default=False, alias="Is Template")
    default_branch: str = Field(default="", alias="Default Branch")

    @classmethod
    def from_github_dict(cls, data: dict[str, Any]) -> "RepoReportItem":
        license_data = data.get("license") or {}
        license_spdx = (
            license_data.get("spdx_id") if isinstance(license_data, dict) else ""
        )

        desc = data.get("description")
        clean_desc = (desc.replace("\n", " ").strip()) if isinstance(desc, str) else ""

        topics = data.get("topics") or []

        return cls(
            name=str(data.get("name") or ""),
            description=clean_desc,
            url=str(data.get("html_url") or ""),
            created_at=str(data.get("created_at") or ""),
            updated_at=str(data.get("updated_at") or ""),
            homepage=str(data.get("homepage") or ""),
            size=int(data.get("size") or 0),
            stars=int(data.get("stargazers_count") or 0),
            forks=int(data.get("forks_count") or 0),
            issues=int(data.get("open_issues_count") or 0),
            watchers=int(data.get("watchers_count") or 0),
            language=str(data.get("language") or ""),
            license=str(license_spdx) if license_spdx else "",
            topics=str(topics),
            has_issues=bool(data.get("has_issues")),
            has_projects=bool(data.get("has_projects")),
            has_downloads=bool(data.get("has_downloads")),
            has_wiki=bool(data.get("has_wiki")),
            has_pages=bool(data.get("has_pages")),
            has_discussions=bool(data.get("has_discussions")),
            is_fork=bool(data.get("fork")),
            is_archived=bool(data.get("archived")),
            is_template=bool(data.get("is_template")),
            default_branch=str(data.get("default_branch") or ""),
        )


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
        """Search repositories using GitHub Search API."""
        ...


class CsvWriterService:
    """Service responsible specifically for writing Pydantic models to CSV."""

    async def write_models_to_csv(self, path: Path, items: Sequence[BaseModel]) -> None:
        if not items:
            async with aiofiles.open(path, "w", encoding="utf-8") as f:
                await f.write("")
            return

        headers = [field.alias or name for name, field in items[0].model_fields.items()]

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=headers)
        writer.writeheader()

        for item in items:
            writer.writerow(item.model_dump(by_alias=True))

        async with aiofiles.open(path, "w", encoding="utf-8", newline="") as f:
            await f.write(buf.getvalue())


class GitHubReposExportService:
    """Service that orchestrates fetching data and delegating CSV writing."""

    def __init__(
        self,
        github_client: GitHubSearchClient,
        csv_writer: CsvWriterService,
        static_dir: Path,
    ) -> None:
        self._github = github_client
        self._csv_writer = csv_writer
        self._static_dir = static_dir

    def _build_query_string(self, params: RepoSearchParams) -> str:
        parts: list[str] = [f"language:{params.lang}"]

        for t in params.topics:
            t_clean = t.strip().lower()
            if t_clean:
                parts.append(f"topic:{t_clean}")

        if params.stars_max is None:
            parts.append(f"stars:>={params.stars_min}")
        else:
            parts.append(f"stars:{params.stars_min}..{params.stars_max}")

        if params.forks_max is None:
            parts.append(f"forks:>={params.forks_min}")
        else:
            parts.append(f"forks:{params.forks_min}..{params.forks_max}")

        return " ".join(parts)

    async def export(self, search_params: RepoSearchParams) -> Path:
        """
        Fetch repositories from GitHub search API and write them to a CSV file.
        """
        limit = max(0, search_params.limit)
        offset = max(0, search_params.offset)

        self._static_dir.mkdir(parents=True, exist_ok=True)

        topics_suffix = ""
        if search_params.topics:
            safe_topics = "-".join(
                [t.strip().lower() for t in search_params.topics if t.strip()]
            )
            if safe_topics:
                topics_suffix = f"_topics-{safe_topics}"[:80]

        filename = f"repositories_{search_params.lang}_{limit}_{offset}{topics_suffix}.csv"
        output_path = self._static_dir / filename

        if limit == 0:
            await self._write_empty_csv_with_headers(output_path)
            return output_path

        api_max_window = 1000
        fetch_end_index = min(offset + limit, api_max_window)
        items_needed_count = max(0, fetch_end_index - offset)

        if items_needed_count == 0:
            await self._write_empty_csv_with_headers(output_path)
            return output_path

        query_string = self._build_query_string(search_params)

        per_page = 100
        first_page = offset // per_page + 1
        last_page = (fetch_end_index - 1) // per_page + 1

        all_raw_items: list[dict[str, Any]] = []
        for page in range(first_page, last_page + 1):
            resp = await self._github.search_repositories(
                q=query_string,
                page=page,
                per_page=per_page,
                sort=search_params.sort,
                order=search_params.order,
            )
            all_raw_items.extend(resp.items)

        start_slice = offset - (first_page - 1) * per_page
        sliced_raw_items = all_raw_items[
            start_slice : start_slice + items_needed_count
        ]

        report_items = [RepoReportItem.from_github_dict(item) for item in sliced_raw_items]

        if not report_items:
            await self._write_empty_csv_with_headers(output_path)
            return output_path

        await self._csv_writer.write_models_to_csv(output_path, report_items)
        return output_path

    async def _write_empty_csv_with_headers(self, path: Path) -> None:
        """Helper to satisfy tests expecting headers even when rows are empty."""
        headers = [field.alias or name for name, field in RepoReportItem.model_fields.items()]
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=headers)
        writer.writeheader()
        async with aiofiles.open(path, "w", encoding="utf-8", newline="") as f:
            await f.write(buf.getvalue())
