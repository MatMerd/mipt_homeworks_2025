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


class SearchParams(BaseModel):
    limit: int
    offset: int = 0
    lang: str
    stars_min: int = 0
    stars_max: int | None = None
    forks_min: int = 0
    forks_max: int | None = None


class SearchResponse(BaseModel):
    filename: str
    total_found: int
    saved_count: int
    message: str
