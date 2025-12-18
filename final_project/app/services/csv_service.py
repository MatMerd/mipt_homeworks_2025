import csv
import io
from typing import Any

from aiofile import async_open


CSV_HEADERS = [
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


async def write_csv(
    filepath: str,
    rows: list[dict[str, Any]],
) -> None:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_HEADERS)
    writer.writeheader()
    writer.writerows(rows)

    async with async_open(filepath, "w", encoding="utf-8") as f:
        await f.write(output.getvalue())


def generate_filename(lang: str, limit: int, offset: int) -> str:
    return f"repositories_{lang}_{limit}_{offset}.csv"
