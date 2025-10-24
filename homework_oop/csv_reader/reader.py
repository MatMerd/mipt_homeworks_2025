import csv
from typing import TextIO


class CSVReader:
    __slots__ = ("__file", "__data")

    def __init__(self, filepath: str) -> None:
        try:
            self.__file: TextIO = open(filepath, mode='r', encoding='utf-8')
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден по пути {filepath}")
        except Exception as e:
            print(f"Произошла ошибка при чтении файла: {e}")

        self.__data: list[dict] | None = None

    @staticmethod
    def __try_convert(value: str) -> int | float | str | None:
        if value is None or value == '':
            return value

        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                return value

    def read(self) -> None:
        csv_reader = csv.DictReader(self.__file)
        self.__data = [row for row in csv_reader]

        for row in self.__data:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = self.__try_convert(value)

    def get_data(self) -> list[dict]:
        return self.__data.copy()

    def __del__(self) -> None:
        self.__file.close()
