from __future__ import annotations

from typing import Any


def safe_slug(value: str) -> str:
    import re

    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return cleaned or "unknown"


def get_license_spdx_id(repo: dict[str, Any]) -> str:
    license_obj = repo.get("license")
    if isinstance(license_obj, dict):
        spdx = license_obj.get("spdx_id")
        if isinstance(spdx, str) and spdx and spdx != "NOASSERTION":
            return spdx
    return ""


def get_topics_as_list_str(repo: dict[str, Any]) -> str:
    topics = repo.get("topics")
    if isinstance(topics, list):
        safe = [t for t in topics if isinstance(t, str)]
        return str(safe)
    return "[]"


def repo_to_csv_row(repo: dict[str, Any]) -> list[object]:
    return [
        repo.get("name", ""),
        repo.get("description", ""),
        repo.get("html_url", ""),
        repo.get("created_at", ""),
        repo.get("updated_at", ""),
        repo.get("homepage", ""),
        repo.get("size", 0),
        repo.get("stargazers_count", 0),
        repo.get("forks_count", 0),
        repo.get("open_issues_count", 0),
        repo.get("watchers_count", 0),
        repo.get("language", ""),
        get_license_spdx_id(repo),
        get_topics_as_list_str(repo),
        repo.get("has_issues", False),
        repo.get("has_projects", False),
        repo.get("has_downloads", False),
        repo.get("has_wiki", False),
        repo.get("has_pages", False),
        repo.get("has_discussions", False),
        repo.get("fork", False),
        repo.get("archived", False),
        repo.get("is_template", False),
        repo.get("default_branch", ""),
    ]
