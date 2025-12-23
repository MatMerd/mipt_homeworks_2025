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

    def __init__(self, github_client: GitHubClient) -> None:
        self._github_client = github_client
        self._ensure_static_dir()

    def _ensure_static_dir(self) -> None:
        os.makedirs(self.STATIC_DIR, exist_ok=True)

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
        per_page = 100
        page = 1

        while len(repositories) < limit:
            repos_batch = await self._github_client.search_repositories_as_models(
                query=query,
                sort="stars",
                order="desc",
                per_page=per_page,
                page=page,
            )

            if not repos_batch:
                break

            repositories.extend(repos_batch)

            if len(repositories) >= limit:
                break

            page += 1

        result_repos = repositories[offset : offset + limit]

        for idx, repo in enumerate(result_repos):
            repo.position_cur = offset + idx + 1

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        filepath = self.STATIC_DIR / filename

        await self._write_csv(filepath, result_repos)

        return str(filepath)

    async def _write_csv(self, filepath: Path, repositories: list[Repository]) -> None:

        lines = [Repository.csv_header()]
        lines.extend(repo.to_csv_row() for repo in repositories)
        content = "".join(lines)

        async with async_open(filepath, "w") as f:
            await f.write(content)

