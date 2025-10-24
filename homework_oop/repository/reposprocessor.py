from typing import Dict, Any, List
import copy

from homework_oop.repository.query import Query
from homework_oop.repository.errors import FilterError, SortingError, GroupingError
from homework_oop.repository.repomodel import Repository
from homework_oop.statistics_saver import StatisticsSaver


class ReposProcessor:
    @staticmethod
    def execute(
        data: List[Repository], user_id: int, query: Query
    ) -> Dict[Any, List[Repository]]:
        result: List[Repository] = copy.copy(data)
        if query.filters:
            result = ReposProcessor._apply_filters(result, query.filters)

        if query.sort_by:
            result = ReposProcessor._apply_sorting(result, query.sort_by)

        ReposProcessor._calc_stats(copy.copy(result), user_id)

        if query.group_by:
            return ReposProcessor._apply_grouping(result, query.group_by)
        else:
            return {"": result}

    @staticmethod
    def _calc_stats(repos: List[Repository], user_id: int) -> List[List[Repository]]:
        statistics_saver: StatisticsSaver = StatisticsSaver("user_stats.json")
        size_results: List[Repository] = statistics_saver.median(user_id, repos, "Size")
        max_liked: List[Repository] = statistics_saver.max(
            user_id, repos, "Stars", limit=1
        )
        no_lang_repos: List[Repository] = statistics_saver.select_by_predicate(
            user_id, repos, "Language", lambda x: x == ""
        )
        max_watchers_repos: List[Repository] = statistics_saver.max(
            user_id, repos, "Watchers", limit=10
        )
        archived_repos: List[Repository] = statistics_saver.select_by_predicate(
            user_id, repos, "Is_Archived", lambda x: x, limit=10
        )
        statistics_saver.save()
        return [
            size_results,
            max_liked,
            no_lang_repos,
            max_watchers_repos,
            archived_repos,
        ]

    @staticmethod
    def _apply_filters(
        repos: List[Repository], filters: Dict[str, Any]
    ) -> List[Repository]:
        try:
            filtered = repos
            if filters is None:
                return repos
            for field, value in filters.items():
                filtered = [repo for repo in filtered if repo.get_field(field) == value]
            return filtered
        except Exception as e:
            raise FilterError(filters, e)

    @staticmethod
    def _apply_sorting(repos: List[Repository], sort_by: str) -> List[Repository]:
        try:
            if not repos or sort_by is None:
                return repos

            return sorted(repos, key=lambda x: x.get_field(sort_by))
        except Exception as e:
            raise SortingError(sort_by, e)

    @staticmethod
    def _apply_grouping(
        repos: List[Repository], group_by: str
    ) -> Dict[Any, List[Repository]]:
        try:
            if group_by is None:
                return {"": repos}
            groups: Dict[Any, List[Repository]] = {}
            for repo in repos:
                value: Any = repo.get_field(group_by)
                if value not in groups:
                    groups[value] = []
                groups[value].append(repo)
            return groups
        except Exception as e:
            raise GroupingError(group_by, e)
