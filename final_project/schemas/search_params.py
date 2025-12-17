from pydantic import BaseModel, Field
from typing import Optional, Annotated


class SearchParams(BaseModel):
    lang: Annotated[
        str,
        Field(
            description="Язык программирования",
            example="Python"
        )
    ]

    limit: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Количество репозиториев"
    )

    offset: int = Field(
        default=0,
        ge=0,
        description="Смещение (для пагинации)"
    )

    stars_min: int = Field(
        default=0,
        ge=0,
        description="Минимальное количество звезд"
    )

    stars_max: Optional[int] = Field(
        default=None,
        ge=0,
        description="Максимальное количество звезд"
    )

    forks_min: int = Field(
        default=0,
        ge=0,
        description="Минимальное количество форков"
    )

    forks_max: Optional[int] = Field(
        default=None,
        ge=0,
        description="Максимальное количество форков"
    )
