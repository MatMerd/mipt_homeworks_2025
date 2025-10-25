import csv
from typing import List, Dict, Type, Any


class ReaderCSV:
    def __init__(self, filepath: str, model: Dict[str, Type], encoding: str = "utf-8"):
        self.filepath = filepath
        self.model = model
        self.encoding = encoding

    def __enter__(self):
        data: List[Dict[str, Any]] = []

        with open(self.filepath, mode="r", newline="", encoding=self.encoding) as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(self._map_to_model(row))
        return data

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def _map_to_model(self, row: Dict[str, str]) -> Dict[str, Any]:
        if len(row) != len(self.model):
            raise ValueError("The number of fields does not match the model!")

        cast_data: Dict[str, Any] = {}
        for key in row:
            if key not in self.model:
                raise ValueError(f"There is no field in the model: {key}")
            try:
                cast_data[key] = self.model[key](row[key])
            except Exception as e:
                raise ValueError(
                    f"Error casting field '{key}' to {self.model[key]}: {e}"
                )
        return cast_data
