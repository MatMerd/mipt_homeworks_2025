from dataclasses import dataclass
from enum import Enum
from typing import List

class SortOrder(Enum):
    ASCENDING = 1
    DESCENDING = 2

@dataclass
class Repository:
    name: str
    description: str
    url: str
    created_at: str
    updated_at: str
    homepage: str
    size: int
    stars: int
    forks: int
    issues: int
    watchers: int
    language: str
    license: str
    topics: List[str]
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    is_fork: bool
    is_archived: bool
    is_template: bool
    default_branch: str
