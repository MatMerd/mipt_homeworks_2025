from typing import Any
import aiofiles


class CsvExporter:
    async def export_to_csv(self, repositories: list[dict[str, Any]], filename: str) -> str:
        filepath = f"static/{filename}"
        rows = []
        for repo in repositories:
            rows.append(
                {
                    "name": repo.get("name", ""),
                    "owner": repo.get("owner", {}).get("login", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "language": repo.get("language", ""),
                    "url": repo.get("html_url", ""),
                    "description": repo.get("description", ""),
                    "created_at": repo.get("created_at", ""),
                    "updated_at": repo.get("updated_at", ""),
                }
            )
        async with aiofiles.open(filepath, "w", encoding="utf-8", newline="") as f:
            if rows:
                fieldnames = list(rows[0].keys())
                header = ",".join(fieldnames) + "\n"
                await f.write(header)
                for row in rows:
                    line = ",".join(
                        f'"{str(value).replace(chr(34), chr(34) + chr(34))}"'
                        for value in row.values()
                    )
                    await f.write(line + "\n")
        return filepath
