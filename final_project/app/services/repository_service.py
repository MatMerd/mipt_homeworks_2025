import os

from aiofile import async_open

from app.infrastructure.github_client import github_client
from app.models import Repository, SearchParams, SearchResponse
from app.settings import settings


class RepositoryService:
    def __init__(self) -> None:
        self.client = github_client
        self.static_dir = settings.static_dir

    def build_query(self, params: SearchParams) -> str:
        query_parts: list[str] = []

        query_parts.append(f"language:{params.lang}")

        if params.stars_max is not None:
            query_parts.append(f"stars:{params.stars_min}..{params.stars_max}")
        elif params.stars_min > 0:
            query_parts.append(f"stars:>={params.stars_min}")

        if params.forks_max is not None:
            query_parts.append(f"forks:{params.forks_min}..{params.forks_max}")
        elif params.forks_min > 0:
            query_parts.append(f"forks:>={params.forks_min}")

        return " ".join(query_parts)

    def get_filename(self, lang: str, limit: int, offset: int) -> str:
        return f"repositories_{lang}_{limit}_{offset}.csv"

    async def save_to_csv(self, repositories: list[Repository], filename: str) -> str:
        os.makedirs(self.static_dir, exist_ok=True)
        filepath = os.path.join(self.static_dir, filename)

        csv_header = (
            "name,full_name,html_url,description,language,"
            "stargazers_count,forks_count,watchers_count,"
            "open_issues_count,created_at,updated_at"
        )

        lines = [csv_header]
        for repo in repositories:
            description = (repo.description or "").replace('"', '""').replace("\n", " ")
            line = (
                f'"{repo.name}","{repo.full_name}","{repo.html_url}",'
                f'"{description}","{repo.language or ""}",'
                f"{repo.stargazers_count},{repo.forks_count},{repo.watchers_count},"
                f'{repo.open_issues_count},"{repo.created_at}","{repo.updated_at}"'
            )
            lines.append(line)

        content = "\n".join(lines)

        async with async_open(filepath, "w", encoding="utf-8") as f:
            await f.write(content)

        return filepath

    async def search_and_save(self, params: SearchParams) -> SearchResponse:
        query = self.build_query(params)

        repositories = await self.client.fetch_all_repositories(
            query=query,
            limit=params.limit,
            offset=params.offset,
        )

        filename = self.get_filename(params.lang, params.limit, params.offset)
        filepath = await self.save_to_csv(repositories, filename)

        return SearchResponse(
            filename=filename,
            total_found=len(repositories),
            saved_count=len(repositories),
            message=f"Successfully saved {len(repositories)} repositories to {filepath}",
        )


repository_service = RepositoryService()
