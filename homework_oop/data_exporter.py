import typing as tp
import json
import csv

class DataExporter:
    """
    Класс для экспорта данных в csv или json.
    """
    @staticmethod
    def export_to_json(data: tp.Any, filename: str) -> None:
        if not filename.endswith(".json"):
            filename += ".json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Данные успешно экспортированы в файл {filename}")
        except Exception as e:
            print(f"Произошла ошибка при экспорте данных: {e}")

    @staticmethod
    def export_to_csv(data: tp.Any, filename: str) -> None:
        if not filename.endswith(".csv"):
            filename += ".csv"

        fieldnames = list(data[0].keys())
        try:
            with open(filename, 'w', encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Данные успешно экспортированы в файл {filename}")
        except Exception as e:
            print(f"Произошла ошибка при экспорте данных: {e}")