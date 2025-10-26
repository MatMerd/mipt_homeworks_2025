from dataclasses import dataclass
import heapq

from homework_oop.logger import log_operation


@dataclass
class RepositoryStatistics:
    repositories: list

    @property
    def total_repos(self):
        return len(self.repositories)

    @property
    def median_size(self):
        if not self.repositories:
            return 0.0
        sizes = [repo.size for repo in self.repositories]
        sorted_sizes = sorted(sizes)
        n = len(sorted_sizes)
        mid = n // 2
        return (sorted_sizes[mid - 1] + sorted_sizes[mid]) / 2 if n % 2 == 0 else sorted_sizes[mid]

    @property
    def most_starred(self):
        if not self.repositories:
            return None
        return max(self.repositories, key=lambda repo: repo.stars)

    @property
    def repos_without_language(self):
        return [repo for repo in self.repositories if not repo.language]

    @property
    def total_stars(self):
        return sum(repo.stars for repo in self.repositories)

    @property
    def avg_stars(self):
        return self.total_stars / self.total_repos if self.total_repos > 0 else 0

    @property
    def language_distribution(self):
        distribution = {}
        for repo in self.repositories:
            language = repo.language or 'Unknown'
            distribution[language] = distribution.get(language, 0) + 1
        return distribution

    @log_operation
    def top_repos_by_commits(self, top_n=10):
        sorted_repos = sorted(self.repositories, key=lambda x: x.forks, reverse=True)
        return sorted_repos[:top_n]

    @log_operation
    def top_repos_by_stars(self, top_n=10):
        return heapq.nlargest(top_n, self.repositories, key=lambda x: x.stars)

    @log_operation
    def top_repos_by_activity(self, top_n=10):
        return heapq.nlargest(top_n, self.repositories, key=lambda x: x.activity_score)