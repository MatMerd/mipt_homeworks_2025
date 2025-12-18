import os
from pathlib import Path

from aiofile import async_open

from src.infrastructure.github_client import GitHubClient
from src.models import Repository


def _build_query(
    lang: str,
    stars_min: int = 0,
    stars_max: int | None = None,
    forks_min: int = 0,
    forks_max: int | None = None,
) -> str:
    query_parts = [f"language:{lang}"]

    if stars_max is not None:
        query_parts.append(f"stars:{stars_min}..{stars_max}")
    else:
        query_parts.append(f"stars:>={stars_min}")

    if forks_max is not None:
        query_parts.append(f"forks:{forks_min}..{forks_max}")
    else:
        query_parts.append(f"forks:>={forks_min}")

    return " ".join(query_parts)


class RepositorySearchService:
    STATIC_DIR = Path("static")
    CSV_HEADER = "Repo,Owner,Position Cur,Position Prev,Stars,Watchers,Forks,Open Issues,Language\n"

    def __init__(self, github_client: GitHubClient) -> None:
        self._github_client = github_client

    async def search_and_save(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
    ) -> str:
        query = _build_query(
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )

        repositories: list[Repository] = []

        total_needed = offset + limit
        per_page = 100

        page = 1
        while len(repositories) < total_needed:
            response = await self._github_client.search_repositories(
                query=query,
                sort="stars",
                order="desc",
                per_page=per_page,
                page=page,
            )

            items = response.get("items", [])
            if not items:
                break

            for idx, item in enumerate(items):
                position = (page - 1) * per_page + idx + 1
                repo = Repository.from_github_item(item, position)
                repositories.append(repo)

                if len(repositories) >= total_needed:
                    break

            page += 1

        result_repos = repositories[offset : offset + limit]
        for idx, repo in enumerate(result_repos):
            repo.position_cur = idx + 1

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        filepath = self.STATIC_DIR / filename

        os.makedirs(self.STATIC_DIR, exist_ok=True)

        await self._write_csv(filepath, result_repos)

        return str(filepath)

    async def _write_csv(self, filepath: Path, repositories: list[Repository]) -> None:
        async with async_open(filepath, "w") as f:
            await f.write(self.CSV_HEADER)

            for repo in repositories:
                position_prev = repo.position_prev if repo.position_prev is not None else ""
                line = (
                    f"{repo.repo},{repo.owner},{repo.position_cur},{position_prev},"
                    f"{repo.stars},{repo.watchers},{repo.forks},{repo.open_issues},"
                    f"{repo.language or ''}\n"
                )
                await f.write(line)
