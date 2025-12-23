import ast
import csv
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from github_stars.services.github_repos.service import (
    GitHubReposExportService,
    RepoSearchParams,
)


class _GitHubClientWithCalls(Protocol):
    calls: list[tuple[str, int, int, str, str]]


async def _read_rows(path: Path) -> tuple[Sequence[str] | None, list[dict[str, str]]]:
    with Path.open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


async def test_export_limit_zero_writes_header_only(
    github_repos_export_service: GitHubReposExportService,
) -> None:
    """Limit=0 should create a CSV file with header only."""
    p = RepoSearchParams(
        limit=0,
        offset=0,
        lang="Python",
        stars_min=0,
        stars_max=None,
        forks_min=0,
        forks_max=None,
        topics=[],
    )
    out = await github_repos_export_service.export(p)

    fields, rows = await _read_rows(out)
    assert fields is not None
    assert rows == []


async def test_export_slices_correctly(
    github_repos_export_service: GitHubReposExportService,
) -> None:
    """Export should return exactly `limit` repos starting from `offset`."""
    p = RepoSearchParams(
        limit=50,
        offset=120,
        lang="Python",
        stars_min=0,
        stars_max=None,
        forks_min=0,
        forks_max=None,
        topics=[],
    )
    out = await github_repos_export_service.export(p)

    _, rows = await _read_rows(out)
    assert len(rows) == 50
    assert rows[0]["Name"] == "repo120"
    assert rows[-1]["Name"] == "repo169"


async def test_export_offset_outside_1000_window_returns_empty(
    github_repos_export_service: GitHubReposExportService,
) -> None:
    """
    Offset beyond first 1000 results should.

    return an empty CSV (current implementation limit).
    """
    p = RepoSearchParams(
        limit=10,
        offset=1500,
        lang="Python",
        stars_min=0,
        stars_max=None,
        forks_min=0,
        forks_max=None,
        topics=[],
    )
    out = await github_repos_export_service.export(p)
    _, rows = await _read_rows(out)
    assert rows == []


async def test_export_replaces_newlines_in_description(
    github_repos_export_service: GitHubReposExportService,
) -> None:
    """Ensure CSV description field has no newlines."""
    p = RepoSearchParams(
        limit=1,
        offset=0,
        lang="Python",
        stars_min=0,
        stars_max=None,
        forks_min=0,
        forks_max=None,
        topics=[],
    )
    out = await github_repos_export_service.export(p)

    _, rows = await _read_rows(out)
    assert len(rows) == 1
    assert "\n" not in rows[0]["Description"]
    assert rows[0]["Description"] == "line1 line2"


async def test_export_filters_by_topics(
    github_repos_export_service: GitHubReposExportService,
    fake_github_client: _GitHubClientWithCalls,
) -> None:
    """Export uses topics in query and keeps them in CSV output.

    Service should add `topic:<name>` qualifiers to the GitHub query.
    CSV rows should contain the requested topic in the `Topics` column.
    """
    p = RepoSearchParams(
        limit=12,
        offset=0,
        lang="Python",
        topics=["a"],
        stars_min=0,
        stars_max=None,
        forks_min=0,
        forks_max=None,
    )
    out = await github_repos_export_service.export(p)

    _, rows = await _read_rows(out)
    assert len(rows) == 12

    for row in rows:
        topics = ast.literal_eval(row["Topics"])
        assert "a" in topics

    assert any("topic:a" in q for (q, *_rest) in fake_github_client.calls)
