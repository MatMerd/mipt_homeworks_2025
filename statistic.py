from collections import Counter
import statistics


class Statistic:

    @staticmethod
    def get_size_median(repositories):
        if not repositories:
            return None

        sizes = [repo.size for repo in repositories if repo.size is not None]
        if not sizes:
            return None

        return int(statistics.median(sizes))

    @staticmethod
    def get_most_starred_repo(repositories):
        if not repositories:
            return None

        return max(
            repositories,
            key=lambda repo: repo.stars if repo.stars is not None else 0,
        )

    @staticmethod
    def get_repos_without_language(repositories):
        return [
            repo for repo in repositories
            if not repo.language
        ]

    @staticmethod
    def get_top_repos_by_forks(repositories):
        sorted_repos = sorted(
            repositories,
            key=lambda repo: repo.forks if repo.forks is not None else 0,
            reverse=True
        )

        return sorted_repos[:10]

    @staticmethod
    def get_language_statistics(repositories):
        languages = [
            repo.language if repo.language is not None else 'Unknown'
            for repo in repositories
        ]

        return dict(Counter(languages))

    def get_all_statistics(self, repositories):
        stats = {}

        stat1 = self.get_size_median(repositories)
        stat2 = self.get_most_starred_repo(repositories)
        stat3 = self.get_repos_without_language(repositories)
        stat4 = self.get_top_repos_by_forks(repositories)
        stat5 = self.get_language_statistics(repositories)

        stats['size_median'] = stat1
        stats['most_starred'] = stat2
        stats['without_language'] = stat3
        stats['top_forks'] = stat4
        stats['language_stat'] = stat5

        return stats
