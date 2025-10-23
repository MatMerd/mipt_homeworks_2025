import csv
from typing import List, Dict, Any


class CSVReader:
    def __init__(self, filename: str, encoding: str = 'utf-8', delimiter: str = ',') -> None:
        """
        :param filename: название csv файла
        :param encoding: кодировка файла
        :param delimiter: разделитель полей
        """
        self.filename = filename
        self.encoding = encoding
        self.delimiter = delimiter
        self._data = None

    def read_as_dict(self) -> List[Dict[str, Any]]:
        """
        Считывает csv файл
        :return: Данные файла в виде словаря
        """
        data = []
        try:
            with open(self.filename, 'r', encoding=self.encoding) as file:
                reader = csv.DictReader(file, delimiter=self.delimiter)
                data = [row for row in reader]
            self._data = data
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.filename} не найден")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")
