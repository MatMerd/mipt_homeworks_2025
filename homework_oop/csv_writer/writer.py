import json
import csv


class DataExporter:
    def __init__(self, data: dict):
        self.__data: dict = data

    def export(self, fileprefix: str, export_format: str = 'json') -> None:
        export_format = export_format.lower()
        try:
            if export_format == 'json':
                self._save_to_json(fileprefix)
            elif export_format == 'csv':
                self._save_to_csv(fileprefix)
            else:
                raise ValueError(f"Неподдерживаемый формат: '{export_format}'. Используйте 'json' или 'csv'.")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def _save_to_json(self, file_handle):
        for key, value in self.__data.items():
            with open(f"{file_handle}_{key}.json", 'w', encoding='utf-8') as f:
                json.dump(value, f, indent=2, ensure_ascii=False)
            print(f"Данные успешно сохранены в файл {file_handle}_{key}.json")

    def _save_to_csv(self, file_handle):

        for key, value in self.__data.items():
            with open(f"{file_handle}_{key}.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

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
            print(f"Данные успешно сохранены в файл {file_handle}_{key}.csv")