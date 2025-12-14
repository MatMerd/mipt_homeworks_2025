import httpx
from typing import Optional, List, Dict, Any


class GitHubClient:
    BASE_URL = "https://api.github.com/search/repositories"

    async def search_repositories(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int = 0,
        stars_max: Optional[int] = None,
        forks_min: int = 0,
        forks_max: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        query_parts = []

        if lang:
            query_parts.append(f"language:{lang}")

        s_max = stars_max if stars_max is not None else "*"
        query_parts.append(f"stars:{stars_min}..{s_max}")

        f_max = forks_max if forks_max is not None else "*"
        query_parts.append(f"forks:{forks_min}..{f_max}")

        q_string = " ".join(query_parts)

        per_page = min(limit, 100)
        page = (offset // per_page) + 1

        params: dict[str, str | int] = {
            "q": q_string,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        return data.get("items", [])
