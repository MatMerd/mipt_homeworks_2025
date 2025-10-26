import csv
import json
from typing import List, Dict, Any

DATA_PATH = "homework_oop/repositories.csv"


def save_to_csv(filename: str, projection: List[Dict[str, Any]]):
    rows = projection[0].keys()

    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(rows)
        for row in projection:
            writer.writerow(row.values())


def save_to_json(filename: str, projection: List[Dict[str, Any]]):
    with open(filename, "w") as file:
        json.dump(projection, file)
