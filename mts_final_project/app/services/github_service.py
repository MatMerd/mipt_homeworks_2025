import csv
from typing import List
from pathlib import Path
from app.models.github import Repository, SearchParams
from app.infrastructure.github_client import GitHubClient
import asyncio


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()

    def build_search_query(self, params: SearchParams) -> str:
        """Построение поискового запроса для GitHub API"""
        query_parts = []

        if params.lang:
            query_parts.append(f"language:{params.lang}")

        if params.stars_max is not None:
            query_parts.append(f"stars:{params.stars_min}..{params.stars_max}")
        elif params.stars_min > 0:
            query_parts.append(f"stars:>={params.stars_min}")

        if params.forks_max is not None:
            query_parts.append(f"forks:{params.forks_min}..{params.forks_max}")
        elif params.forks_min > 0:
            query_parts.append(f"forks:>={params.forks_min}")

        return " ".join(query_parts) if query_parts else "stars:>0"

    async def search_repositories(self, params: SearchParams) -> List[Repository]:
        """Поиск репозиториев"""
        query = self.build_search_query(params)

        total_needed = params.offset + params.limit
        repos_needed = []
        page = 1

        while len(repos_needed) < total_needed:
            try:
                result = await self.client.search_repositories(
                    query=query, per_page=100, page=page
                )

                if not result.get("items"):
                    break

                for item in result["items"]:
                    repo = self._map_to_repository(item)
                    repos_needed.append(repo)

                if len(repos_needed) >= 1000 or page * 100 >= result["total_count"]:
                    break

                page += 1
                await asyncio.sleep(0.5)

            except Exception:
                break

        start_idx = params.offset if params.offset < len(repos_needed) else 0
        end_idx = min(start_idx + params.limit, len(repos_needed))

        return repos_needed[start_idx:end_idx]

    def _map_to_repository(self, item: dict) -> Repository:
        """Маппинг ответа GitHub API в модель Repository"""
        return Repository(
            name=item.get("name", ""),
            description=item.get("description"),
            url=item.get("html_url", ""),
            created_at=item.get("created_at"),
            updated_at=item.get("updated_at"),
            homepage=item.get("homepage"),
            size=item.get("size", 0),
            stars=item.get("stargazers_count", 0),
            forks=item.get("forks_count", 0),
            issues=item.get("open_issues_count", 0),
            watchers=item.get("watchers_count", 0),
            language=item.get("language"),
            license=item.get("license", {}).get("key") if item.get("license") else None,
            topics=item.get("topics", []),
            has_issues=item.get("has_issues", False),
            has_projects=item.get("has_projects", False),
            has_downloads=item.get("has_downloads", False),
            has_wiki=item.get("has_wiki", False),
            has_pages=item.get("has_pages", False),
            has_discussions=item.get("has_discussions", False),
            is_fork=item.get("fork", False),
            is_archived=item.get("archived", False),
            is_template=item.get("is_template", False),
            default_branch=item.get("default_branch", "main"),
        )

    def save_to_csv(self, repositories: List[Repository], filename: str):
        """Сохранение репозиториев в CSV файл"""
        Path("static").mkdir(exist_ok=True)
        filepath = f"static/{filename}"

        fieldnames = [
            "Name",
            "Description",
            "URL",
            "Created At",
            "Updated At",
            "Homepage",
            "Size",
            "Stars",
            "Forks",
            "Issues",
            "Watchers",
            "Language",
            "License",
            "Topics",
            "Has Issues",
            "Has Projects",
            "Has Downloads",
            "Has Wiki",
            "Has Pages",
            "Has Discussions",
            "Is Fork",
            "Is Archived",
            "Is Template",
            "Default Branch",
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for repo in repositories:
                row = {
                    "Name": repo.name,
                    "Description": repo.description or "",
                    "URL": repo.url,
                    "Created At": repo.created_at.isoformat(),
                    "Updated At": repo.updated_at.isoformat(),
                    "Homepage": repo.homepage or "",
                    "Size": repo.size,
                    "Stars": repo.stars,
                    "Forks": repo.forks,
                    "Issues": repo.issues,
                    "Watchers": repo.watchers,
                    "Language": repo.language or "",
                    "License": repo.license or "",
                    "Topics": ",".join(repo.topics),
                    "Has Issues": repo.has_issues,
                    "Has Projects": repo.has_projects,
                    "Has Downloads": repo.has_downloads,
                    "Has Wiki": repo.has_wiki,
                    "Has Pages": repo.has_pages,
                    "Has Discussions": repo.has_discussions,
                    "Is Fork": repo.is_fork,
                    "Is Archived": repo.is_archived,
                    "Is Template": repo.is_template,
                    "Default Branch": repo.default_branch,
                }
                writer.writerow(row)

        return filepath
