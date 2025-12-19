import math
import os
import csv
import io
from typing import Optional, List, Dict, Any

from aiofile import async_open
from gitfastapi.infrastructure.github_client import GitHubClient

class RepositoryService:
    def __init__(self, client: GitHubClient):
        self.client = client

    async def search_and_save_repositories(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int,
        stars_max: Optional[int],
        forks_min: int,
        forks_max: Optional[int],
    ) -> dict[str, Any]:
        stars_part = f"{stars_min}..{stars_max}" if stars_max is not None else f">={stars_min}"
        forks_part = f"{forks_min}..{forks_max}" if forks_max is not None else f">={forks_min}"
        q = f"language:{lang} stars:{stars_part} forks:{forks_part}"

        page_size = 100
        first_page = offset // page_size + 1
        first_page_offset = offset % page_size
        pages_needed = math.ceil((first_page_offset + limit) / page_size)

        items: List[Dict[str, Any]] = []
        fetched = 0

        for page in range(first_page, first_page + pages_needed):
            data = await self.client.search_repositories(
                query=q,
                page=page,
                per_page=page_size
            )
            page_items = data.get("items", [])
            
            if page == first_page and first_page_offset:
                page_items = page_items[first_page_offset:]

            for repo in page_items:
                if fetched >= limit:
                    break
                items.append(repo)
                fetched += 1

            if fetched >= limit or not page_items:
                break

        os.makedirs("static", exist_ok=True)
        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        csv_path = os.path.join("static", filename)

        fieldnames = [
            "id",
            "name",
            "full_name",
            "html_url",
            "description",
            "language",
            "stargazers_count",
            "forks_count",
            "created_at",
            "updated_at",
        ]

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for repo in items:
            writer.writerow(
                {
                    "id": repo.get("id"),
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "html_url": repo.get("html_url"),
                    "description": repo.get("description"),
                    "language": repo.get("language"),
                    "stargazers_count": repo.get("stargazers_count"),
                    "forks_count": repo.get("forks_count"),
                    "created_at": repo.get("created_at"),
                    "updated_at": repo.get("updated_at"),
                }
            )
        
        content = output.getvalue()
        
        async with async_open(csv_path, "w", encoding="utf-8") as afp:
            await afp.write(content)

        return {
            "saved": len(items),
            "file": csv_path,
            "limit": limit,
            "offset": offset,
            "lang": lang,
        }
