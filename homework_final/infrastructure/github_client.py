import asyncio

import httpx
from typing import Optional, List, Dict, Any


class GitHubClient:
    def __init__(self, base_url: str, api_base_url: str = "https://api.github.com", token: Optional[str] = None):
        self.base_url = base_url
        self.api_base_url = api_base_url
        self.token = token

    async def search_repositories(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int = 0,
        stars_max: Optional[int] = None,
        forks_min: int = 0,
        forks_max: Optional[int] = None,
        contributor: Optional[str] = None,
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

        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])

            if not contributor:
                return items

            contributor_lc = contributor.lower()
            sem = asyncio.Semaphore(10)

            async def repo_has_contributor(repo: Dict[str, Any]) -> bool:
                full_name = repo.get("full_name")
                if not full_name:
                    return False

                url = f"{self.api_base_url}/repos/{full_name}/contributors"
                async with sem:
                    r = await client.get(url, params={"per_page": 100, "page": 1})
                    if r.status_code == 404:
                        return False
                    r.raise_for_status()
                    contributors = r.json() or []
                    return any((c.get("login") or "").lower() == contributor_lc for c in contributors)

            checks = await asyncio.gather(*(repo_has_contributor(repo) for repo in items))
            filtered = [repo for repo, ok in zip(items, checks) if ok]
        return filtered
