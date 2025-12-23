from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, PositiveInt, model_validator


class SearchRepositoriesParams(BaseModel):
    """Query params for GitHub repositories search."""

    limit: PositiveInt = Field(description="How many repositories to return")
    offset: int = Field(
        default=0, ge=0, description="Offset from the beginning of results"
    )
    lang: str = Field(min_length=1, description="Repository language")

    stars_min: int = Field(default=0, ge=0, description="Minimum number of stars")
    stars_max: int | None = Field(
        default=None, ge=0, description="Maximum number of stars"
    )
    forks_min: int = Field(default=0, ge=0, description="Minimum number of forks")
    forks_max: int | None = Field(
        default=None, ge=0, description="Maximum number of forks"
    )
    license: str | None = Field(
        default=None,
        min_length=1,
        description="License type (e.g., mit, apache-2.0, gpl-3.0)",
    )

    @model_validator(mode="after")
    def validate_ranges(self) -> SearchRepositoriesParams:
        """Validate min/max ranges consistency."""
        if self.stars_max is not None and self.stars_max < self.stars_min:
            raise ValueError("stars_max must be >= stars_min")
        if self.forks_max is not None and self.forks_max < self.forks_min:
            raise ValueError("forks_max must be >= forks_min")
        return self


class SearchRepositoriesResponse(BaseModel):
    """Endpoint response."""

    csv_path: Path = Field(description="Saved CSV file path")
    returned: int = Field(ge=0, description="How many rows were written")
