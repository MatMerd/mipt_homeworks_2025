from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Repository:
    name: str
    description: str
    url: str
    created_at: datetime
    updated_at: datetime
    homepage: str
    size: int
    stars: int
    forks: int
    issues: int
    watchers: int
    language: str
    license: str
    topics: list = field(default_factory=list)
    has_issues: bool = False
    has_projects: bool = False
    has_downloads: bool = False
    has_wiki: bool = False
    has_pages: bool = False
    has_discussions: bool = False
    is_fork: bool = False
    is_archived: bool = False
    is_template: bool = False
    default_branch: str = "main"

    @property
    def is_popular(self):
        return self.stars > 1000

    @property
    def age_days(self):
        return (datetime.now() - self.created_at).days

    @property
    def activity_score(self):
        return (self.stars * 0.4 + self.forks * 0.3 + self.watchers * 0.3)

    def __str__(self):
        return f"{self.name} ({self.stars} stars, {self.language})"