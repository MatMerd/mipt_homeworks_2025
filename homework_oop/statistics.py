import csv
import json
from typing import List, Dict, Any, Optional


class Statistics:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data = data

    def get_median(self) -> float:
        sizes = [int(item['Size']) for item in self.data]
        return (min(sizes) + max(sizes)) / 2

    def get_most_liked(self) -> Dict[str, Any]:
        return max(self.data, key=lambda x: int(x['Stars']))

    def get_repos_without_language(self) -> List[Dict[str, Any]]:
        return list(filter(lambda x: x['Language'] == '', self.data))

    def get_top10_most_commited(self) -> List[Dict[str, Any]]:
        return sorted(self.data, key=lambda x: int(x['Forks']), reverse=True)[:10]

    def save_to_csv(self, filename: str, data: Optional[List[Dict[str, Any]]] = None) -> None:
        if data is None:
            data = self.data

        if not data:
            raise ValueError("Нет данных для сохранения")

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def save_to_json(self, filename: str, data: Optional[List[Dict[str, Any]]] = None) -> None:
        if data is None:
            data = self.data

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)