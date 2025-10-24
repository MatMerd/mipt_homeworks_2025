import csv, ast
from typing import Dict, List
from .models import Repository

class CSVRepositoryReader:
    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.repositories: List[Repository] = []

    def read_from_file(self, filepath: str = None) -> List[Repository]:
        if filepath:
            self.filepath = filepath
        if not self.filepath:
            raise ValueError("Файл не указан")
        with open(self.filepath, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            return [self._parse_row(row) for row in reader]

    def _parse_row(self, row: Dict[str, str]) -> Repository:
        topics_str = row.get('Topics', '[]')
        try:
            topics = ast.literal_eval(topics_str)
        except Exception:
            topics = []
        def parse_bool(val: str): return val.strip().lower() == 'true'
        return Repository(
            name=row.get('Name', ''),
            size=int(row.get('Size', 0)),
            stars=int(row.get('Stars', 0)),
            forks=int(row.get('Forks', 0)),
            language=row.get('Language', ''),
            topics=topics,
            is_fork=parse_bool(row.get('Is_Fork', 'False')),
            is_archived=parse_bool(row.get('Is_Archived', 'False')),
            is_template=parse_bool(row.get('Is_Template', 'False')),
            license=row.get('License', ''),
            description=row.get('Description', ''),
            url=row.get('URL', ''),
            created_at=row.get('Created_At', ''),
            updated_at=row.get('Updated_At', ''),
            homepage=row.get('Homepage', ''),
            issues=int(row.get('Issues', 0)),
            watchers=int(row.get('Watchers', 0)),
            has_issues=parse_bool(row.get('Has_Issues', 'False')),
            has_projects=parse_bool(row.get('Has_Projects', 'False')),
            has_downloads=parse_bool(row.get('Has_Downloads', 'False')),
            has_wiki=parse_bool(row.get('Has_Wiki', 'False')),
            has_pages=parse_bool(row.get('Has_Pages', 'False')),
            has_discussions=parse_bool(row.get('Has_Discussions', 'False')),
            default_branch=row.get('Default_Branch', 'main'),
        )
