from typing import Any
from ..utils.file_context import AsyncFileContext
from ..utils.batching import batch_repositories
import logging

logger = logging.getLogger("exporter")


class CsvExporter:
    async def export_to_csv(self, repositories: list[dict[str, Any]], filename: str) -> str:
        filepath = f"static/{filename}"
        transformed_repos = []
        for repo in repositories:
            transformed_repos.append({
                "name": repo.get("name", ""),
                "owner": repo.get("owner", {}).get("login", ""),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", ""),
                "url": repo.get("html_url", ""),
                "description": repo.get("description", ""),
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
            })

        async with AsyncFileContext(filepath, mode="w", encoding="utf-8", newline="") as f:
            if transformed_repos:
                fieldnames = list(transformed_repos[0].keys())
                header = ",".join(fieldnames) + "\n"
                await f.write(header)
                for batch in batch_repositories(transformed_repos, batch_size=1000):
                    for row in batch:
                        line = ",".join(
                            f'"{str(value).replace(chr(34), chr(34) + chr(34))}"'
                            for value in row.values()
                        )
                        await f.write(line + "\n")

                logger.info(f"Exported {len(transformed_repos)} repositories to {filepath}")

        return filepath