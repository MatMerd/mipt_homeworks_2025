from pydantic import BaseModel, Field, model_validator
from typing import Optional


class SearchRepositoriesRequest(BaseModel):
    limit: int = Field(..., ge=1, le=1000, description="Number of repositories to return")
    offset: int = Field(0, ge=0, description="Number of repositories to skip")
    lang: Optional[str] = Field(None, description="Programming language")
    stars_min: int = Field(0, ge=0, description="Minimum stars")
    stars_max: Optional[int] = Field(None, ge=0, description="Maximum stars")
    forks_min: int = Field(0, ge=0, description="Minimum forks")
    forks_max: Optional[int] = Field(None, ge=0, description="Maximum forks")

    @model_validator(mode='after')
    def validate_ranges(self):
        if self.stars_max is not None and self.stars_max < self.stars_min:
            raise ValueError("stars_max must be greater than or equal to stars_min")
        if self.forks_max is not None and self.forks_max < self.forks_min:
            raise ValueError("forks_max must be greater than or equal to forks_min")
        return self


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    owner: dict  # Simplified, can be expanded
    html_url: str
    description: Optional[str]
    language: Optional[str]
    stargazers_count: int
    forks_count: int
    created_at: str
    updated_at: str


class SearchResponse(BaseModel):
    total_count: int
    incomplete_results: bool
    items: list[Repository]
