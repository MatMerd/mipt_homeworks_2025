import csv
from homework_oop.repository import Repository
from pathlib import Path
from typing import List


class CSVRepositoryReader:
    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.path = self._get_file_path(file_path)
        self.encoding = encoding
        self.data: List[Repository] = []

    def read(self) -> "CSVRepositoryReader":
        repositories: list[Repository] = []
        with self.path.open(encoding=self.encoding) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                repositories.append(Repository.from_csv_row(row))
        self.data = repositories
        return self

    def get_data(self) -> list[Repository]:
        return list(self.data)

    def _get_file_path(self, file_path: str) -> Path:
        path = Path(file_path)
        self._check_file_path(path)
        return path

    def _check_file_path(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")
