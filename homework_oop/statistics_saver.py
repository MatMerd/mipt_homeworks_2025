from dataclasses import asdict

from .repository.repomodel import Repository
from .statistics import RepositoryStatistics
import json
from typing import Dict, List, Callable


class StatisticsSaver:
    def __init__(self, filepath: str, encoding: str = "utf-8"):
        self.filepath = filepath
        self.encoding = encoding
        self.history: Dict[int, List] = {}

    def _save_result(self, user_id: int, result: List[Repository]) -> List[Repository]:
        dict_repos = []
        for repo in result:
            dict_repos.append(asdict(repo))
        self.history[user_id] = dict_repos
        return result

    def min(
        self, user_id: int, data: List[Repository], field: str, limit: int = -1
    ) -> List[Repository]:
        result = RepositoryStatistics.min(data, field, limit)
        return self._save_result(user_id, result)

    def max(
        self, user_id: int, data: List[Repository], field: str, limit: int = -1
    ) -> List[Repository]:
        result = RepositoryStatistics.max(data, field, limit)
        return self._save_result(user_id, result)

    def median(self, user_id: int, data: List[Repository], field: str):
        result = RepositoryStatistics.median(data, field)
        return self._save_result(user_id, result)

    def select_by_predicate(
        self,
        user_id: int,
        data: List[Repository],
        field: str,
        predicate: Callable,
        limit: int = -1,
    ):
        result = RepositoryStatistics.select_by_predicate(data, field, predicate, limit)
        return self._save_result(user_id, result)

    def selection_by_value(
        self,
        user_id: int,
        data: List[Repository],
        field: str,
        value: int | float,
        eps: int | float,
        limit: int = -1,
    ):
        result = RepositoryStatistics.selection_by_value(data, field, value, eps, limit)
        return self._save_result(user_id, result)

    def save(self):
        with open(self.filepath, "w", encoding=self.encoding) as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
