import statistics
from collections import Counter
from entity.repository import Repository
from typing import Any


class Statistic:

    @staticmethod
    def __get_size_median(repositories: list[Repository]) -> int | None:
        if not repositories:
            return None

        sizes = [repo.size for repo in repositories if repo.size is not None]
        if not sizes:
            return None

        return int(statistics.median(sizes))

    @staticmethod
    def __get_most_starred_repo(repositories: list[Repository]) -> Repository | None:
        if not repositories:
            return None

        return max(
            repositories,
            key=lambda repo: repo.stars if repo.stars is not None else 0,
        )

    @staticmethod
    def __get_repos_without_language(repositories: list[Repository]) -> list[Repository]:
        return [
            repo for repo in repositories
            if not repo.language
        ]

    @staticmethod
    def __get_top_repos_by_forks(repositories: list[Repository]) -> list[Repository]:
        sorted_repos = sorted(
            repositories,
            key=lambda repo: repo.forks if repo.forks is not None else 0,
            reverse=True
        )

        return sorted_repos[:10]

    @staticmethod
    def __get_language_statistics(repositories: list[Repository]) -> dict[str, int]:
        languages = [
            repo.language if repo.language != '' else 'Unknown'
            for repo in repositories
        ]

        return dict(Counter(languages))

    @staticmethod
    def get_all_statistics(repositories: list[Repository]) -> dict[str, Any]:
        stats = {}

        stat1 = Statistic.__get_size_median(repositories)
        stat2 = Statistic.__get_most_starred_repo(repositories)
        stat3 = Statistic.__get_repos_without_language(repositories)
        stat4 = Statistic.__get_top_repos_by_forks(repositories)
        stat5 = Statistic.__get_language_statistics(repositories)

        stats['size_median'] = stat1
        stats['most_starred'] = stat2
        stats['without_language'] = stat3
        stats['top_forks'] = stat4
        stats['language_stat'] = stat5

        return stats
