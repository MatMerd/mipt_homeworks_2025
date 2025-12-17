from __future__ import annotations

import csv
import io
from collections.abc import Iterable
from pathlib import Path

from aiofile import AIOFile, Writer

from homework_fastapi.services.csv_schema import CSV_HEADER


async def write_repositories_csv(path: Path, rows: Iterable[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.StringIO()
    csv_writer = csv.writer(buffer, lineterminator="\n")
    async with AIOFile(path, "w", encoding="utf-8") as afp:
        writer = Writer(afp)
        csv_writer.writerow(CSV_HEADER)
        await writer(buffer.getvalue())
        buffer.seek(0)
        buffer.truncate(0)
        for row in rows:
            csv_writer.writerow(row)
            await writer(buffer.getvalue())
            buffer.seek(0)
            buffer.truncate(0)
