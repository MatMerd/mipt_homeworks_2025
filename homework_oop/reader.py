import csv
from homework_oop.repository import Repository
from pathlib import Path
from typing import List


class CSVRepositoryReader:
    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.file_path = file_path
        self.encoding = encoding
        self.data: List[Repository] = []

    def read(self) -> "CSVRepositoryReader":
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")

        repositories: list[Repository] = []
        with path.open(encoding=self.encoding) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                repositories.append(Repository.from_csv_row(row))
        self.data = repositories
        return self

    def get_data(self) -> list[Repository]:
        return list(self.data)
