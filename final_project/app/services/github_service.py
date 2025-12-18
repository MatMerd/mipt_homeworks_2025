from typing import Any


def build_search_query(
    lang: str,
    stars_min: int,
    stars_max: int | None,
    forks_min: int,
    forks_max: int | None,
) -> str:
    parts = [f"language:{lang}"]

    if stars_max is not None:
        parts.append(f"stars:{stars_min}..{stars_max}")
    else:
        parts.append(f"stars:>={stars_min}")

    if forks_max is not None:
        parts.append(f"forks:{forks_min}..{forks_max}")
    else:
        parts.append(f"forks:>={forks_min}")

    return " ".join(parts)


def map_repository_to_row(repo: dict[str, Any]) -> dict[str, Any]:
    license_info = repo.get("license")
    license_name = license_info.get("key", "") if license_info else ""

    topics = repo.get("topics", [])
    topics_str = str(topics) if topics else "[]"

    return {
        "Name": repo.get("name", ""),
        "Description": (repo.get("description") or "").replace("\n", " "),
        "URL": repo.get("html_url", ""),
        "Created At": repo.get("created_at", ""),
        "Updated At": repo.get("updated_at", ""),
        "Homepage": repo.get("homepage") or "",
        "Size": repo.get("size", 0),
        "Stars": repo.get("stargazers_count", 0),
        "Forks": repo.get("forks_count", 0),
        "Issues": repo.get("open_issues_count", 0),
        "Watchers": repo.get("watchers_count", 0),
        "Language": repo.get("language") or "",
        "License": license_name,
        "Topics": topics_str,
        "Has Issues": repo.get("has_issues", False),
        "Has Projects": repo.get("has_projects", False),
        "Has Downloads": repo.get("has_downloads", False),
        "Has Wiki": repo.get("has_wiki", False),
        "Has Pages": repo.get("has_pages", False),
        "Has Discussions": repo.get("has_discussions", False),
        "Is Fork": repo.get("fork", False),
        "Is Archived": repo.get("archived", False),
        "Is Template": repo.get("is_template", False),
        "Default Branch": repo.get("default_branch", ""),
    }


async def fetch_repositories(
    client: Any,
    query: str,
    limit: int,
    offset: int,
) -> list[dict[str, Any]]:
    all_repos: list[dict[str, Any]] = []
    total_needed = limit + offset
    page = 1
    per_page = 100

    while len(all_repos) < total_needed:
        data = await client.search_repositories(query, per_page=per_page, page=page)
        items = data.get("items", [])

        if not items:
            break

        all_repos.extend(items)
        page += 1

        if len(items) < per_page:
            break

    repos_with_offset = all_repos[offset : offset + limit]
    return [map_repository_to_row(repo) for repo in repos_with_offset]
