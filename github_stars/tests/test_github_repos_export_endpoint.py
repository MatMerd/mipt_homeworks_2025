import ast
import csv
from pathlib import Path

from httpx import AsyncClient
from starlette import status


async def test_export_endpoint_creates_csv(client: AsyncClient) -> None:
    """Export endpoint should create a CSV file with the requested number of rows."""
    resp = await client.get(
        "/api/github-repos/export",
        params={
            "limit": 5,
            "offset": 0,
            "lang": "Python",
            "stars_min": 0,
            "forks_min": 0,
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert "path" in data

    path = Path(data["path"])
    assert path.exists()

    with Path.open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 5


async def test_export_endpoint_validation_missing_lang(client: AsyncClient) -> None:
    """Endpoint should require the `lang` query parameter."""
    resp = await client.get(
        "/api/github-repos/export", params={"limit": 5, "offset": 0}
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_export_endpoint_validation_negative_limit(client: AsyncClient) -> None:
    """Endpoint should reject negative limit via FastAPI validation."""
    resp = await client.get(
        "/api/github-repos/export",
        params={"limit": -1, "offset": 0, "lang": "Python"},
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_export_endpoint_topics_filter(client: AsyncClient) -> None:
    """Endpoint accepts `topics` and writes them into the exported CSV.

    When `topics` is provided, exported rows should include that topic in the
    `Topics` column.
    """
    resp = await client.get(
        "/api/github-repos/export",
        params={
            "limit": 6,
            "offset": 0,
            "lang": "Python",
            "stars_min": 0,
            "forks_min": 0,
            "topics": ["a"],
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()

    path = Path(data["path"])
    with Path.open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 6
    for row in rows:
        topics = ast.literal_eval(row["Topics"])
        assert "a" in topics
