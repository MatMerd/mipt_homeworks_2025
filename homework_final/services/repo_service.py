import csv
import os
from typing import Optional
from homework_final.infrastructure.github_client import GitHubClient


class RepositoryService:
    def __init__(self, client: GitHubClient, static_dir: str = "static"):
        self.client = client
        self.static_dir = static_dir

        os.makedirs(self.static_dir, exist_ok=True)

    async def fetch_and_save_repos(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int,
        stars_max: Optional[int],
        forks_min: int,
        forks_max: Optional[int],
    ) -> str:
        repos = await self.client.search_repositories(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        filepath = os.path.join(self.static_dir, filename)

        fieldnames = [
            "name",
            "stargazers_count",
            "forks_count",
            "language",
            "html_url",
            "description",
        ]

        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for repo in repos:
                row = {field: repo.get(field) for field in fieldnames}
                writer.writerow(row)

        return filepath
