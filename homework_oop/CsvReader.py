import csv


class CsvReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []
        self.headers = []

    def read(self):
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            self.data = list(reader)
        return self.data