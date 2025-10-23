import csv
import os
import datetime

class CSVLoader:
    def __init__(self, filename, delimiter=',', auto_typization=True):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found.")
        self.filename = filename
        self.delimiter = delimiter
        self.auto_typization = auto_typization
        self.header = []
        self.rows = []
        self.field_idx = {}

    def _auto_type(self, value, flag):
        if not self.auto_typization or not isinstance(value, str) or flag:
            return value
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError:
            return value

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=self.delimiter)
            self.header = next(reader)
            self.field_idx = {name: i for i, name in enumerate(self.header)}
            self.rows = [
                tuple(self._auto_type(row[i], i < 2) for i in range(len(row)))
                for row in reader
            ]