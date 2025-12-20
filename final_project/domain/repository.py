from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any


@dataclass(frozen=True, slots=True)
class Repository:
    """Repository row in the CSV format from the first homework."""

    name: str = ""
    description: str | None = None
    url: str = ""
    created_at: str = ""
    updated_at: str = ""
    homepage: str | None = None
    size: int = 0
    stars: int = 0
    forks: int = 0
    issues: int = 0
    watchers: int = 0
    language: str | None = None
    license: str | None = None
    topics: list[str] = field(default_factory=list)
    has_issues: bool = False
    has_projects: bool = False
    has_downloads: bool = False
    has_wiki: bool = False
    has_pages: bool = False
    has_discussions: bool = False
    is_fork: bool = False
    is_archived: bool = False
    is_template: bool = False
    default_branch: str = ""

    @staticmethod
    def attr_to_csv_key(name: str) -> str:
        """Convert dataclass attribute name to CSV column name."""
        if name == "url":
            return "URL"
        return name.replace("_", " ").title()

    @classmethod
    def csv_header(cls) -> list[str]:
        """Return CSV header in the expected order."""
        return [cls.attr_to_csv_key(field_info.name) for field_info in fields(cls)]

    def as_csv_dict(self) -> dict[str, object]:
        """Return CSV row as a dict with CSV header keys."""
        return {
            self.attr_to_csv_key(field_info.name): getattr(self, field_info.name)
            for field_info in fields(self)
        }

    @staticmethod
    def coerce_topics(value: Any) -> list[str]:
        """Normalize topics to a list of strings."""
        if isinstance(value, list):
            return [str(topic) for topic in value]
        return []

    @classmethod
    def from_github_item(cls, item: dict[str, Any]) -> Repository:
        """Convert GitHub search API item into Repository."""

        def get_required_string(key: str) -> str:
            return str(item.get(key) or "")

        def get_optional_string(key: str) -> str | None:
            value = item.get(key)
            return value or None

        def get_int(key: str) -> int:
            return int(item.get(key) or 0)

        def get_bool(key: str) -> bool:
            return bool(item.get(key) or False)

        license_info = item.get("license") or {}
        license_spdx_id = license_info.get("spdx_id") or None

        return cls(
            name=get_required_string("name"),
            description=get_optional_string("description"),
            url=get_required_string("html_url"),
            created_at=get_required_string("created_at"),
            updated_at=get_required_string("updated_at"),
            homepage=get_optional_string("homepage"),
            size=get_int("size"),
            stars=get_int("stargazers_count"),
            forks=get_int("forks_count"),
            issues=get_int("open_issues_count"),
            watchers=get_int("watchers_count"),
            language=get_optional_string("language"),
            license=license_spdx_id,
            topics=cls.coerce_topics(item.get("topics")),
            has_issues=get_bool("has_issues"),
            has_projects=get_bool("has_projects"),
            has_downloads=get_bool("has_downloads"),
            has_wiki=get_bool("has_wiki"),
            has_pages=get_bool("has_pages"),
            has_discussions=get_bool("has_discussions"),
            is_fork=get_bool("fork"),
            is_archived=get_bool("archived"),
            is_template=get_bool("is_template"),
            default_branch=get_required_string("default_branch"),
        )
