from dataclasses import dataclass, field
from typing import Any, Optional, Dict


@dataclass
class Repository:
    name: str = ""
    description: Optional[str] = None
    url: str = ""
    created_at: str = ""
    updated_at: str = ""
    homepage: Optional[str] = None
    size: int = 0
    stars: int = 0
    forks: int = 0
    issues: int = 0
    watchers: int = 0
    language: Optional[str] = None
    license: Optional[str] = None
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

    @classmethod
    def from_csv_row(cls, row: Dict[str, Any]) -> "Repository":
        def safe_str_required(value: Any) -> str:
            if value is None:
                return ""
            text = str(value).strip()
            return text

        def safe_str_optional(value: Any) -> Optional[str]:
            if value is None:
                return None
            text = str(value).strip()
            return text

        def safe_int(value: Any) -> int:
            if value is None:
                return 0
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0

        def safe_bool(value: Any) -> bool:
            if value is None:
                return False
            text = str(value).strip().lower()
            return text == "true"

        def safe_topics(value: Any) -> list[str]:
            if isinstance(value, list):
                return [str(x) for x in value]
            if isinstance(value, str):
                text = value.strip()
                if not text or text == "[]":
                    return []
                cleaned = text.strip("[]").replace("'", "").replace('"', "")
                if not cleaned:
                    return []
                return [tag.strip() for tag in cleaned.split(",") if tag.strip()]
            return []

        return cls(
            name=safe_str_required(row.get("Name")),
            description=safe_str_optional(row.get("Description")),
            url=safe_str_required(row.get("URL")),
            created_at=safe_str_required(row.get("Created At")),
            updated_at=safe_str_required(row.get("Updated At")),
            homepage=safe_str_optional(row.get("Homepage")),
            size=safe_int(row.get("Size")),
            stars=safe_int(row.get("Stars")),
            forks=safe_int(row.get("Forks")),
            issues=safe_int(row.get("Issues")),
            watchers=safe_int(row.get("Watchers")),
            language=safe_str_optional(row.get("Language")),
            license=safe_str_optional(row.get("License")),
            topics=safe_topics(row.get("Topics")),
            has_issues=safe_bool(row.get("Has Issues")),
            has_projects=safe_bool(row.get("Has Projects")),
            has_downloads=safe_bool(row.get("Has Downloads")),
            has_wiki=safe_bool(row.get("Has Wiki")),
            has_pages=safe_bool(row.get("Has Pages")),
            has_discussions=safe_bool(row.get("Has Discussions")),
            is_fork=safe_bool(row.get("Is Fork")),
            is_archived=safe_bool(row.get("Is Archived")),
            is_template=safe_bool(row.get("Is Template")),
            default_branch=safe_str_required(row.get("Default Branch")),
        )

    @staticmethod
    def csv_key_to_attr(name: str) -> str:
        return name.strip().lower().replace(" ", "_")

    @staticmethod
    def attr_to_csv_key(name: str) -> str:
        if name == "url":
            return "URL"
        return name.replace("_", " ").title()
