import csv
from pathlib import Path

from final_project.final_project.infrastructure.github_client import GitHubClient


class RepositoryService:
    """Service that fetches repositories from GitHub and exports them to CSV."""

    def __init__(self, client: GitHubClient, static_dir: str | Path = "static") -> None:
        self.client = client
        self.static_dir = Path(static_dir)
        self.static_dir.mkdir(parents=True, exist_ok=True)

    async def fetch_and_save_repos(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int,
        stars_max: int | None,
        forks_min: int,
        forks_max: int | None,
        contributor: str | None = None,
    ) -> str:
        """Fetch repositories and save them to a CSV file."""
        repos = await self.client.search_repositories(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
            contributor=contributor,
        )

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        filepath = self.static_dir / filename

        fieldnames = [
            "name",
            "stargazers_count",
            "forks_count",
            "language",
            "html_url",
            "description",
        ]

        with filepath.open(mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for repo in repos:
                row = {field: repo.get(field) for field in fieldnames}
                writer.writerow(row)

        return str(filepath)
