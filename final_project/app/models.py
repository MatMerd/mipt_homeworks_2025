import msgspec
from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    full_name: str
    html_url: str
    description: str | None
    language: str | None
    stargazers_count: int
    forks_count: int
    watchers_count: int
    open_issues_count: int
    created_at: str
    updated_at: str
    contributors_count: int | None = None


class SearchParams(BaseModel):
    limit: int
    offset: int = 0
    lang: str
    stars_min: int = 0
    stars_max: int | None = None
    forks_min: int = 0
    forks_max: int | None = None
    contributors_min: int = 0
    contributors_max: int | None = None


class SearchResponse(BaseModel):
    filename: str
    total_found: int
    saved_count: int
    message: str


class GitHubSearchParams(msgspec.Struct):
    q: str
    sort: str = "stars"
    order: str = "desc"
    per_page: int = 100
    page: int = 1
