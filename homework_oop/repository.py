from datetime import datetime
from typing import Any

import constants


class Repository:
    def __init__(self, values: list[str]) -> None:
        self._string_format: list[str] = values
        self._initialize(values)

    def _initialize(self, values: list[str]) -> None:
        (
            name,
            description,
            url,
            created_at,
            updated_at,
            home_page,
            size,
            stars,
            forks,
            issues,
            watchers,
            language,
            license,
            topics,
            has_issues,
            has_projects,
            has_downloads,
            has_wiki,
            has_pages,
            has_discussions,
            is_fork,
            is_archived,
            is_template,
            default_branch,
        ) = values
        self.name: str = name
        self.description: str = description
        self.url: str = url
        self.created_at: datetime = datetime.fromisoformat(
            created_at.replace("Z", "+00:00")
        )
        self.updated_at: datetime = datetime.fromisoformat(
            updated_at.replace("Z", "+00:00")
        )
        self.home_page: str = home_page
        self.size = int(size)
        self.stars: int = int(stars)
        self.forks: int = int(forks)
        self.issues: int = int(issues)
        self.watchers: int = int(watchers)
        self.language: str = language
        self.license: str = license
        self.topics: Any = topics
        self.has_issues: bool = self.to_bool(has_issues)
        self.has_projects: bool = self.to_bool(has_projects)
        self.has_downloads: bool = self.to_bool(has_downloads)
        self.has_wiki: bool = self.to_bool(has_wiki)
        self.has_pages: bool = self.to_bool(has_pages)
        self.has_discussions: bool = self.to_bool(has_discussions)
        self.is_fork: bool = self.to_bool(is_fork)
        self.is_archived: bool = self.to_bool(is_archived)
        self.is_template: bool = self.to_bool(is_template)
        self.default_branch: str = default_branch

    def __repr__(self) -> str:
        return (
            f"Repository(\n"
            f"  name='{self.name}',\n"
            f"  description='{self.description[:50]}...',\n"
            f"  url='{self.url}',\n"
            f"  created_at={self.created_at},\n"
            f"  updated_at={self.updated_at},\n"
            f"  home_page='{self.home_page}',\n"
            f"  size={self.size},\n"
            f"  stars={self.stars},\n"
            f"  forks={self.forks},\n"
            f"  issues={self.issues},\n"
            f"  watchers={self.watchers},\n"
            f"  language='{self.language}',\n"
            f"  license='{self.license}',\n"
            f"  topics={self.topics},\n"
            f"  has_issues={self.has_issues},\n"
            f"  has_projects={self.has_projects},\n"
            f"  has_downloads={self.has_downloads},\n"
            f"  has_wiki={self.has_wiki},\n"
            f"  has_pages={self.has_pages},\n"
            f"  has_discussions={self.has_discussions},\n"
            f"  is_fork={self.is_fork},\n"
            f"  is_archived={self.is_archived},\n"
            f"  is_template={self.is_template},\n"
            f"  default_branch='{self.default_branch}'\n"
            f")"
        )

    @staticmethod
    def to_bool(st: str) -> bool:
        return st.strip().lower() == "true"

    def _get_repository_field_by_name(self, field_name: str) -> Any:
        return self.__getattribute__(field_name)

    def to_string(self, separator: str):
        return separator.join(self._string_format)

    def to_map(self) -> dict[str, str]:
        res = dict()
        for field in constants.all_fields_ordered:
            res[field] = str(self._get_repository_field_by_name(field))
        return res
