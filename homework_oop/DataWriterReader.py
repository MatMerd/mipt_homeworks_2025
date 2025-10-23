import csv
import json
from typing import List, Dict, Any


class DataReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[Dict[str, Any]] = []

    def read(self) -> List[Dict[str, Any]]:
        with open(self.file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            self.data = [row for row in reader]
        return self.data


class DataWriter:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def save_csv(self, file_path: str):
        fieldnames = self.data[0].keys()
        with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",")
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

    def save_json(self, file_path: str):
        with open(file_path, mode="w", encoding="utf-8") as jsonfile:
            json.dump(self.data, jsonfile, ensure_ascii=False, indent=4)
