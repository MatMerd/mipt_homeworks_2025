from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SearchParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    lang: str
    stars_min: int = Field(default=0, ge=0)
    stars_max: Optional[int] = None
    forks_min: int = Field(default=0, ge=0)
    forks_max: Optional[int] = None


class Repository(BaseModel):
    name: str
    description: Optional[str]
    url: str
    created_at: datetime
    updated_at: datetime
    homepage: Optional[str]
    size: int
    stars: int
    forks: int
    issues: int
    watchers: int
    language: Optional[str]
    license: Optional[str]
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
