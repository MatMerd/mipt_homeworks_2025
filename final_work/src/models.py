from pydantic import BaseModel


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
