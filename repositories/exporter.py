import csv
import json
from typing import Any, List, Dict

from .models import Repository


class StatisticsExporter:    
    @staticmethod
    def export_to_csv(statistics_data: Dict[str, Any], filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Metric', 'Value'])
            
            for key, value in statistics_data.items():
                if isinstance(value, list):
                    for idx, item in enumerate(value, 1):
                        if isinstance(item, tuple):
                            writer.writerow([f"{key}_{idx}", f"{item}: {item}"])
                        else:
                            writer.writerow([f"{key}_{idx}", str(item)])
                else:
                    writer.writerow([key, value])
        
        print(f"Статистика экспортирована в CSV: {filepath}")
    
    @staticmethod
    def export_to_json(statistics_data: Dict[str, Any], filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(statistics_data, json_file, ensure_ascii=False, indent=2)
        print(f"Статистика экспортирована в JSON: {filepath}")
    
    @staticmethod
    def export_repositories_to_csv(repositories: List[Repository], filepath: str) -> None:
        if not repositories:
            print("Нет репозиториев для экспорта")
            return
        
        fieldnames = ['Name', 'Description', 'URL', 'Stars', 'Forks', 
                     'Language', 'License', 'Size', 'Is_Fork', 'Is_Archived']
        
        with open(filepath, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for repo in repositories:
                writer.writerow({
                    'Name': repo.name,
                    'Description': repo.description,
                    'URL': repo.url,
                    'Stars': repo.stars,
                    'Forks': repo.forks,
                    'Language': repo.language,
                    'License': repo.license,
                    'Size': repo.size,
                    'Is_Fork': repo.is_fork,
                    'Is_Archived': repo.is_archived
                })
        
        print(f"Экспортировано {len(repositories)} репозиториев в CSV: {filepath}")