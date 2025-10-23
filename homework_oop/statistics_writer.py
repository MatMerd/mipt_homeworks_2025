import json
import csv
import os
from typing import List, Dict, Any, Union
from datetime import datetime


class StatWriter:
    def __init__(self, statistics: Dict[str, Any]):
        self.statistics = statistics

    def export_to_json(self, filename: str = None) -> str:
        """
        Экспортирует статистики в json файл
        :param filename: название файла
        :return:
        """
        if filename is None:
            filename = f"repository_statistics.json"

        if not filename.endswith('.json'):
            filename += '.json'

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.statistics, f, ensure_ascii=False, default=str)

            return filename

        except Exception as e:
            raise Exception(f"Ошибка при сохранении в JSON: {e}")

    def export_to_csv(self, filename: str = None) -> str:
        """
        Экспортирует статистики в csv файл
        :param filename: название файла
        :return:
        """
        if filename is None:
            filename = f"repository_statistics.csv"

        if not filename.endswith('.csv'):
            filename += '.csv'

        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)

                writer.writerow(['Metric', 'Value'])

                self._write_dict_to_csv(writer, self.statistics)

            return filename

        except Exception as e:
            raise Exception(f"Ошибка при сохранении в CSV: {e}")

    def _write_dict_to_csv(self, writer, data: Dict[str, Any], prefix: str = ""):
        """
        Записывает вложенные структуры в csv
        :return:
        """
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                self._write_dict_to_csv(writer, value, full_key)
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    writer.writerow([full_key, json.dumps(value, default=str)])
                else:
                    writer.writerow([full_key, ', '.join(map(str, value))])
            else:
                writer.writerow([full_key, value])
