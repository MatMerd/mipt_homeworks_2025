import csv
from entity.repository import Repository


class Reader:
    @staticmethod
    def read_file(path: str = "homework_oop/repositories.csv") -> list[Repository]:
        with open(path, "r", newline="", encoding='utf-8') as file:
            reader = csv.reader(file)
            repositories = []
            next(reader)
            for row in reader:
                repositories.append(Repository(*row))

        return repositories
