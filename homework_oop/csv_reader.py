import csv


class CSVReader:
    def read(self, file_name: str) -> list[list[str]]:
        result = []
        with open(file_name, "r", encoding="utf-8") as f:
            file = csv.reader(f)
            next(file)
            for line in file:
                result.append(line)
        return result
