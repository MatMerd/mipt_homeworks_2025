import csv
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Protocol, TypeVar

from homework_oop.src.dto import BaseDTO

T = TypeVar("T", bound=BaseDTO)


@dataclass(slots=True, kw_only=True)
class BaseRepository(Protocol[T]):
    """Base repository protocol."""

    def read(self, model: type[T]) -> list[T]:
        """Read data from repository."""
        ...


@dataclass(slots=True, kw_only=True)
class FileRepository(BaseRepository[T]):
    """File-based repository."""

    file_path: InitVar[str | Path]
    _file_path: Path = field(init=False)

    def __post_init__(self, file_path: str | Path) -> None:
        self._file_path = file_path if isinstance(file_path, Path) else Path(file_path)
        if not self._file_path.is_file():
            raise FileNotFoundError(f"No such file {file_path}")


@dataclass(slots=True, kw_only=True)
class CsvRepository(FileRepository[T]):
    """CSV file repository."""

    _delimiter: str = ","

    def read(self, model: type[T]) -> list[T]:
        """Read data from CSV file."""
        result = []
        with self._file_path.open() as file:
            reader = csv.reader(file, delimiter=self._delimiter)
            next(reader)
            for line in reader:
                result.append(model.build(line))
        return result
