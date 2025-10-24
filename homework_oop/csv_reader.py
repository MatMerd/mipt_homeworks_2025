import csv
from typing import Any, Dict, List


class RepositoryCSVReader:
    """
    Класс для чтения данных из файла

    Fields:
        filename - имя файла для считывания данных
        data - данные файла в преобразованном формате
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.data = []

    def read_all(self) -> List[Dict[str, Any]]:
        """
        Считывание входного файла

        Returns:
            Информация о репозиториях в формате списка словарей
        Raises:
            FileNotFoundError: если файл не найден
        """

        self.data = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                self.data = list(csv_reader)
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.filename} не найден")