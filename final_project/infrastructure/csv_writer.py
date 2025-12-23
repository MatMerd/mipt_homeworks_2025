from __future__ import annotations

import csv
import io
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from aiofile import async_open

from final_project.domain.repository import Repository


@dataclass(frozen=True, slots=True)
class RepositoryCsvWriter:
    """Write repositories to CSV in the format of the first homework."""

    def header(self) -> list[str]:
        """Return CSV header in the expected order."""
        return Repository.csv_header()

    async def write(self, *, path: Path, repositories: Iterable[Repository]) -> int:
        """Write repositories to CSV and return number of written rows."""
        path.parent.mkdir(parents=True, exist_ok=True)
        header = self.header()

        async with async_open(path, "w", encoding="utf-8") as file:
            written = 0
            await file.write(self._csv_line(header))

            for repo in repositories:
                row_dict = repo.as_csv_dict()
                row = [self._cell(row_dict[key]) for key in header]
                await file.write(self._csv_line(row))
                written += 1

        return written

    @staticmethod
    def _csv_line(row: Sequence[object]) -> str:
        buffer = io.StringIO()
        csv.writer(buffer).writerow(row)
        return buffer.getvalue()

    @staticmethod
    def _cell(value: object) -> object:
        if value is None:
            return ""
        if isinstance(value, list):
            return repr(value)
        return value


def get_csv_writer() -> RepositoryCsvWriter:
    """Get CSV writer instance."""
    return RepositoryCsvWriter()
