import csv
import json
from entity.repository import Repository
from typing import Any


class FileManager:
    @staticmethod
    def read_file(path: str = "homework_oop/repositories.csv") -> list[Repository]:
        with open(path, "r", newline="", encoding='utf-8') as file:
            reader = csv.reader(file)
            repositories = []
            next(reader)
            for row in reader:
                repositories.append(Repository(*row))

        return repositories

    @staticmethod
    def write_statistic(statistics: list[dict[str, Any]], path: str = "homework_oop/statistics.json") -> None:
        with open(path, "w", encoding='utf-8') as file:
            json.dump(statistics, file, indent=4, ensure_ascii=False, default=str)
