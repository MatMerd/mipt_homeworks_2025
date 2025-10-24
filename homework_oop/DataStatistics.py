import csv
import json
from collections import Iterable
from statistics import median


class DataStatistics:

    @staticmethod
    def _validate_data(data):
        if not isinstance(data, Iterable) or not all(isinstance(row, dict) for row in data):
            raise TypeError("data должна быть итерируемой коллекцией словарей")

    @staticmethod
    def median_size(data):
        DataStatistics._validate_data(data)

        sizes = [int(row['Size']) for row in data if row.get('Size') and row['Size'].isdigit()]
        return median(sizes) if sizes else None

    @staticmethod
    def max_starred_repo(data):
        DataStatistics._validate_data(data)

        filtered = [row for row in data if row.get('Stars') and row['Stars'].isdigit()]
        if not filtered:
            return []
        max_stars = max(int(row['Stars']) for row in filtered)
        return [row for row in filtered if int(row['Stars']) == max_stars]

    @staticmethod
    def repos_without_language(data):
        DataStatistics._validate_data(data)

        return [row for row in data if not row.get('Language') or not row['Language'].strip()]

    @staticmethod
    def top_commits(data, top_n=10):
        DataStatistics._validate_data(data)

        filtered = [row for row in data if row.get('Forks') and row['Forks'].isdigit()]
        sorted_repos = sorted(filtered, key=lambda x: int(x['Forks']), reverse=True)
        return sorted_repos[:top_n]

    @staticmethod
    def save_statistics(stats, filename, file_format='csv'):
        if file_format == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if isinstance(stats, list) and stats and isinstance(stats[0], dict):
                    keys = stats[0].keys()
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(stats)
                else:
                    f.write(str(stats))
        elif file_format == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=4)
        else:
            raise ValueError("Поддерживаются только форматы csv и json")
