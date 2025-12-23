from pydantic import BaseModel, Field


class RepositorySearchParams(BaseModel):
    limit: int = Field(..., ge=1, le=1000, description="Количество репозиториев")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")
    lang: str = Field(..., description="Язык программирования")
    stars_min: int = Field(0, ge=0, description="Минимальное количество звёзд")
    stars_max: int | None = Field(None, ge=0, description="Максимальное количество звёзд")
    forks_min: int = Field(0, ge=0, description="Минимальное количество форков")
    forks_max: int | None = Field(None, ge=0, description="Максимальное количество форков")


class Repository(BaseModel):
    repo: str
    owner: str
    position_cur: int
    position_prev: int | None = None
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str | None = None

    @classmethod
    def from_github_item(cls, item: dict, position: int) -> "Repository":
        return cls(
            repo=item["name"],
            owner=item["owner"]["login"],
            position_cur=position,
            position_prev=None,
            stars=item["stargazers_count"],
            watchers=item["watchers_count"],
            forks=item["forks_count"],
            open_issues=item["open_issues_count"],
            language=item.get("language"),
        )

    @classmethod
    def csv_header(cls) -> str:
        return "Repo,Owner,Position Cur,Position Prev,Stars,Watchers,Forks,Open Issues,Language\n"

    def to_csv_row(self) -> str:
        position_prev = self.position_prev if self.position_prev is not None else ""
        return (
            f"{self.repo},{self.owner},{self.position_cur},{position_prev},"
            f"{self.stars},{self.watchers},{self.forks},{self.open_issues},"
            f"{self.language or ''}\n"
        )

