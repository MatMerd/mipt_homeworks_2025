from typing import Dict, Any, List
import copy

from homework_oop.repository.query import Query
from homework_oop.repository.errors import FilterError, SortingError, GroupingError
from homework_oop.statistics import RepositoryStatistics


class ReposProcessor:
    def __init__(self, data: List[Dict[str, Any]], user_id: int, query: Query):
        self.data = data
        self.user_id = user_id
        self.query = query

    def execute(self) -> Dict[Any, List[Dict[str, Any]]]:
        result: List[Dict[str, Any]] = copy.copy(self.data)
        if self.query.filters:
            result = self._apply_filters(result)

        if self.query.sort_by:
            result = self._apply_sorting(result)

        self._calc_stats(copy.copy(result))

        if self.query.group_by:
            return self._apply_grouping(result)
        else:
            return {"": result}

    def _calc_stats(self, repos: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        size_results: List[Dict[str, Any]] = RepositoryStatistics.median(repos, "Size")
        max_liked: List[Dict[str, Any]] = RepositoryStatistics.max(
            repos, "Stars", limit=1
        )
        no_lang_repos: List[Dict[str, Any]] = RepositoryStatistics.select_by_predicate(
            repos, "Language", lambda x: x == ""
        )
        max_watchers_repos: List[Dict[str, Any]] = RepositoryStatistics.max(
            repos, "Watchers", limit=10
        )
        archived_repos: List[Dict[str, Any]] = RepositoryStatistics.select_by_predicate(
            repos, "Is Archived", lambda x: x
        )
        return [
            size_results,
            max_liked,
            no_lang_repos,
            max_watchers_repos,
            archived_repos,
        ]

    def _apply_filters(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        try:
            filtered = repos
            if self.query.filters is None:
                return repos
            for field, value in self.query.filters.items():
                filtered = [repo for repo in filtered if repo.get(field) == value]
            return filtered
        except Exception as e:
            raise FilterError(self.query, e)

    def _apply_sorting(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        try:
            if not repos or self.query.sort_by is None:
                return repos
            field_value = repos[0].get(self.query.sort_by)

            sort_field = self.query.sort_by

            if isinstance(field_value, (bool, int, float)):
                return sorted(
                    repos, key=lambda x: float(x.get(sort_field, 0)), reverse=True
                )
            else:
                return sorted(repos, key=lambda x: str(x.get(sort_field, "")))
        except Exception as e:
            raise SortingError(self.query.sort_by, e)

    def _apply_grouping(
        self, repos: List[Dict[str, Any]]
    ) -> Dict[Any, List[Dict[str, Any]]]:
        try:
            if self.query.group_by is None:
                return {"": repos}
            groups: Dict[Any, List[Dict[str, Any]]] = {}
            for repo in repos:
                value: Any = repo[self.query.group_by]
                if value not in groups:
                    groups[value] = []
                groups[value].append(repo)
            return groups
        except Exception as e:
            raise GroupingError(self.query.group_by, e)
