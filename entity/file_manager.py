import csv
from entity.repository import Repository


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
    def write_statistic(statistics: dict[str, str], path: str = "homework_oop/statistics.csv") -> None:
        with open (path, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            writer.writerows(statistics.items())

