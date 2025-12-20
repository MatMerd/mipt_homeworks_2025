from __future__ import annotations

from dataclasses import dataclass, field
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
    def csv_key_to_attr(name: str) -> str:
        """Convert CSV column name to dataclass attribute name."""
        return name.strip().lower().replace(" ", "_")

    @staticmethod
    def attr_to_csv_key(name: str) -> str:
        """Convert dataclass attribute name to CSV column name."""
        if name == "url":
            return "URL"
        return name.replace("_", " ").title()

    @staticmethod
    def coerce_topics(value: Any) -> list[str]:
        """Normalize topics to a list of strings."""
        if isinstance(value, list):
            return [str(x) for x in value]
        return []
