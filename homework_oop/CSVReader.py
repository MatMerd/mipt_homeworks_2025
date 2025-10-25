import csv
from typing import List, Dict

class CSVReader():
    def __init__(self, filepath: str, encoding: str = 'utf-8'):
        self.filepath = filepath
        self.encoding = encoding
        self.column_names: List[str] = []
        self.data: List[Dict[str, str]] = []

    def read(self) -> 'CSVReader':
        with open(self.filepath, 'r', encoding=self.encoding) as file:
            csv_reader = csv.DictReader(file)
            self.column_names = csv_reader.fieldnames
            self.data = [row for row in csv_reader]
        return self
    
    def get_all_data(self) -> List[Dict[str, str]]:
        return self.data
    
    def get_column_names(self) -> List[str]:
        return self.column_names