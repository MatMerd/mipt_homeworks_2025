import csv
import datetime
import json
from typing import Dict, List
from enum import Enum
import statistics

class Method(Enum):
    FILTER = 1
    SORT = 2
    GROUP_BY = 3

class Reader:
    def __init__(self, filename: str, delimier=','):
        self.filename = filename
        self.delimier = delimier

    def read(self) -> List[Dict]:
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=self.delimier)
            return list(reader)


class DataProcessor:
    def __init__(self, data: List[Dict]):
        self.data = data
        self.operations = []

    def filter(self, field: str, value: str, value_type='str'):
        self.validate_field(field)
        converted = self.validate_type(value, value_type)
        self.operations.append((Method.FILTER, field, converted, value_type))
        return self

    def sort(self, field: str, ascending: bool = True, value_type='str'):
        self.validate_field(field)
        self.operations.append((Method.SORT, field, ascending, value_type))
        return self

    def group_by(self, field: str):
        self.validate_field(field)
        self.operations.append((Method.GROUP_BY, field))
        return self

    def execute(self):
        result = self.data
        for op in self.operations:
            if op[0] == Method.FILTER:
                field, value, value_type = op[1], op[2], op[3]
                result = [item for item in result if 
                         self.validate_type(item.get(field), value_type) == value]
            elif op[0] == Method.SORT:
                field, ascending, value_type = op[1], op[2], op[3]
                result = sorted(result, 
                               key=lambda x: self.validate_type(x.get(field), value_type), 
                               reverse=not ascending)
            elif op[0] == Method.GROUP_BY:
                field = op[1]
                groups = {}
                for item in result:
                    key = item.get(field, 'None')
                    groups.setdefault(key, []).append(item)
                result = groups
        return result

    def validate_type(self, value, target_type):
        if target_type == 'int':
            return int(value)
        elif target_type == 'bool':
            return value.lower() == 'true' if isinstance(value, str) else bool(value)
        return value
    
    def validate_field(self, field: str):
        if not self.data or field not in self.data[0]:
            correct_fields = list(self.data[0].keys()) if self.data else []

            similar = [x for x in correct_fields if x.startswith(field)]

            error = f"Field {field} is not available."
            if similar:
                error += f" But there's one similar {similar}"
            raise ValueError(error)
    
class User:
    def __init__(self, name: str):
        self.name = name
        self.saved_queries = {}

    def save_query(self, name: str, processor: DataProcessor):
        self.saved_queries[name] = processor.operations

    def execute_saved_query(self, name: str, data: List[Dict]):
        if name not in self.saved_queries:
            raise KeyError(f"Запрос '{name}' не найден")
        processor = DataProcessor(data)
        processor.operations = self.saved_queries[name]
        return processor.execute()

class Statistics:
    def __init__(self, data):
        self.data = data

    def median_size(self):
        sizes = [int(item['Size']) for item in self.data]
        return statistics.median(sizes) if sizes else 0
    
    def most_popular(self):
        return max(self.data, key=lambda x: int(x['Stars']))
    
    def repos_without_language(self):
        return [item for item in self.data if not item.get('Language') or item['Language'] == '']

    def top_commits(self, top_n=10):
        return sorted(self.data, 
                     key=lambda x: int(x.get('Forks', 0)), 
                     reverse=True)[:top_n]
    
    def save_stats(self, filename: str, format_type: str = 'json'):
        stats = {
            'median_size': self.median_size(),
            'most_popular_repo': self.most_popular()['Name'],
            'most_popular_count': int(self.most_popular()['Stars']),
            'repos_without_language_count': len(self.repos_without_language()),
            'top_commits': [repo['Name'] for repo in self.top_commits()]
        }
        
        if format_type == 'json':
            with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
        elif format_type == 'csv':
            with open(f"{filename}.csv", 'w', encoding='utf-8') as f:
                f.write("statistic,value\n")
                f.write(f"median_size,{stats['median_size']}\n")
                f.write(f"most_popular_repo,{stats['most_popular_repo']}\n")
                f.write(f"most_popular_count,{stats['most_popular_count']}\n")
                f.write(f"repos_without_language_count,{stats['repos_without_language_count']}\n")
                f.write(f"top_commits,{';'.join(stats['top_commits'])}\n")

def main():
    read = Reader("./homework_oop/repositories.csv")
    data = read.read()
    proc = DataProcessor(data)

    ans = proc.filter('Language', 'C++').execute()
    # print(ans)

    stats = Statistics(data)
    print(f"Медианный размер: {stats.median_size()}")
    print(f"Самый популярный репозиторий: {stats.most_popular()['Name']}")
    print(f"Репозиториев без языка: {len(stats.repos_without_language())}")
    stats.save_stats("lox")



if __name__ == "__main__":
    main()
