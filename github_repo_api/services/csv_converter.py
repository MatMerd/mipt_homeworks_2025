import os.path
from pathlib import Path
from typing import Dict, Any, Optional

import pandas as pd


class CSVConverter:
    COLUMNS = [
        'name', 'description', 'url', 'created_at', 'updated_at', 'homepage', 'size', 'stars', 'forks', 'issues', 'watchers', 'language',
        'license', 'topics', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki', 'has_pages', 'has_discussions', 'is_fork', 'is_archived',
        'is_template', 'default_branch'
    ]

    def __init__(self, json_data: Dict[str, Any]):
        self.repos = json_data.get('items', [])

    def _process_filepath(self, filename: str, dirname: Optional[str] = 'static') -> str:
        current_path = Path(__file__).resolve()
        parent_dir = current_path.parent.parent

        return f'{parent_dir}/{dirname}/{filename}'


    def save_csv(self, name: Optional[str] = 'default.csv'):
        df = pd.DataFrame(self.repos)

        existing_columns = [col for col in CSVConverter.COLUMNS if col in df.columns]
        df_filtered = df[existing_columns]

        fullpath = self._process_filepath(name)
        df_filtered.to_csv(fullpath, index=False, encoding='utf-8')
