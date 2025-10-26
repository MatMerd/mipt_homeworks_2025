from datetime import datetime

from homework_oop.logger import log_operation
from models import Repository
from csv_parser import CustomCSVParser


class RepositoryReader:
    TYPE_CONVERTERS = {
        'Size': int,
        'Stars': int,
        'Forks': int,
        'Issues': int,
        'Watchers': int,
        'Has Issues': lambda x: x.lower() == 'true',
        'Has Projects': lambda x: x.lower() == 'true',
        'Has Downloads': lambda x: x.lower() == 'true',
        'Has Wiki': lambda x: x.lower() == 'true',
        'Has Pages': lambda x: x.lower() == 'true',
        'Has Discussions': lambda x: x.lower() == 'true',
        'Is Fork': lambda x: x.lower() == 'true',
        'Is Archived': lambda x: x.lower() == 'true',
        'Is Template': lambda x: x.lower() == 'true',
        'Created At': lambda x: datetime.fromisoformat(x.replace('Z', '+00:00')),
        'Updated At': lambda x: datetime.fromisoformat(x.replace('Z', '+00:00'))
    }

    FIELD_MAPPING = {
        'Name': 'name',
        'Description': 'description',
        'URL': 'url',
        'Created At': 'created_at',
        'Updated At': 'updated_at',
        'Homepage': 'homepage',
        'Size': 'size',
        'Stars': 'stars',
        'Forks': 'forks',
        'Issues': 'issues',
        'Watchers': 'watchers',
        'Language': 'language',
        'License': 'license',
        'Topics': 'topics',
        'Has Issues': 'has_issues',
        'Has Projects': 'has_projects',
        'Has Downloads': 'has_downloads',
        'Has Wiki': 'has_wiki',
        'Has Pages': 'has_pages',
        'Has Discussions': 'has_discussions',
        'Is Fork': 'is_fork',
        'Is Archived': 'is_archived',
        'Is Template': 'is_template',
        'Default Branch': 'default_branch'
    }

    def __init__(self, filename):
        self.filename = filename
        self.parser = CustomCSVParser()

    @log_operation
    def read(self):
        raw_data = self.parser.read_with_headers(self.filename)
        repositories = []

        for row_num, row in enumerate(raw_data, 1):
            try:
                repository_data = self._process_row(row)
                repository = Repository(**repository_data)
                repositories.append(repository)
            except (ValueError, KeyError, TypeError) as e:
                print(f"Ошибка в строке {row_num}: {e}")
                continue

        return repositories

    @log_operation
    def _process_row(self, row):
        processed = {}

        for field, value in row.items():
            if field in self.FIELD_MAPPING:
                target_field = self.FIELD_MAPPING[field]

                if field in self.TYPE_CONVERTERS and value:
                    try:
                        processed[target_field] = self.TYPE_CONVERTERS[field](value)
                    except (ValueError, TypeError) as e:
                        raise ValueError(f"Ошибка преобразования поля '{field}': {value} - {e}")
                else:
                    processed[target_field] = value if value else None

        if 'topics' in processed and processed['topics']:
            topics_str = processed['topics']
            if topics_str.startswith('[') and topics_str.endswith(']'):
                processed['topics'] = [
                    topic.strip("' \"")
                    for topic in topics_str.strip('[]').split(',')
                    if topic.strip("' \"")
                ]
            else:
                processed['topics'] = [topics_str]

        return processed