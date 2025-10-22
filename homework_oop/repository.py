from datetime import *


class Repository:

    name: str
    description: str
    url: str
    created_at: datetime
    updated_at: datetime
    home_page: str
    size: int
    stars: int
    forks: int
    issues: int
    watchers: int
    language: str
    license: str
    topics: list[str]
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

    def __init__(self, values: list[str]) -> None:
        pass

    def _initialize(self, values: list[str]) -> None:
        pass

