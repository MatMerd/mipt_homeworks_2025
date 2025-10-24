import json
import csv


class DataExporter:
    def __init__(self, data: dict):
        self.__data: dict = data

    def export(self, filepath: str, export_format: str = 'json') -> None:
        export_format = export_format.lower()
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if export_format == 'json':
                    self._save_to_json(f)
                elif export_format == 'csv':
                    self._save_to_csv(f)
                else:
                    raise ValueError(f"Неподдерживаемый формат: '{export_format}'. Используйте 'json' или 'csv'.")
            print(f"Данные успешно сохранены в файл {filepath}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def _save_to_json(self, file_handle):
        json.dump(self.__data, file_handle, indent=2, ensure_ascii=False)

    def _save_to_csv(self, file_handle):
        writer = csv.writer(file_handle)

        for key, value in self.__data.items():
            writer.writerow([key])

            if isinstance(value, dict):
                writer.writerow(value.keys())
                writer.writerow(value.values())
            elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
                if not value:
                    continue
                headers = value[0].keys()
                writer.writerow(headers)
                for item in value:
                    writer.writerow(item.values())
            else:
                writer.writerow([value])

            writer.writerow([])