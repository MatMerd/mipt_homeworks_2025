from dataclasses import dataclass
from typing import Dict, Type

repository_model: Dict[str, Type] = {
    "Name": str,
    "Description": str,
    "URL": str,
    "Created At": str,
    "Updated At": str,
    "Homepage": str,
    "Size": int,
    "Stars": int,
    "Forks": int,
    "Issues": int,
    "Watchers": int,
    "Language": str,
    "License": str,
    "Topics": str,
    "Has Issues": bool,
    "Has Projects": bool,
    "Has Downloads": bool,
    "Has Wiki": bool,
    "Has Pages": bool,
    "Has Discussions": bool,
    "Is Fork": bool,
    "Is Archived": bool,
    "Is Template": bool,
    "Default Branch": str,
}


@dataclass
class Repository:
    name: str = ""
    description: str = ""
    url: str = ""
    created_at: str = ""
    updated_at: str = ""
    homepage: str = ""
    size: int = 0
    stars: int = 0
    forks: int = 0
    issues: int = 0
    watchers: int = 0
    language: str = ""
    license: str = ""
    topics: str = ""
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

    def get_field(self, field: str):
        return getattr(self, field.lower())
