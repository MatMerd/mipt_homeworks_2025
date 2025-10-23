import csv


class CSVReader:
    def __init__(self, filename) -> None:
        self.reader = None
        self.filename = filename
        self.fieldnames = []

    def get(self) -> 'CSVReader':
        try:
            with open(self.filename, newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                self.fieldnames = csv_reader.fieldnames
                self.reader = list(csv_reader)
            return self
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл {self.filename} не найден')
        except Exception as e:
            raise Exception(f'Ошибка при чтении файла: {str(e)}')