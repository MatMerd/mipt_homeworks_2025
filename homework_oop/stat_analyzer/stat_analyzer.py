from collections import defaultdict
from statistics import median


class StatisticsCalculator:
    __slots__ = ("__data", "__stats")

    def __init__(self, data: list[dict]):
        self.__data: list[dict] = data
        self.__stats: dict = {}

    def calculate_all(self):
        self.__stats["median_repo_size"] = self._calculate_median_size()
        self.__stats["most_starred_repo"] = self._find_most_starred_repo()
        self.__stats["repos_without_language"] = self._find_repos_without_language()
        self.__stats["top_10_by_commits"] = self._find_top_10_by_commits()
        self.__stats["language_distribution"] = self._calculate_language_distribution()
        return self.__stats

    def _calculate_median_size(self) -> float:
        sizes = [row["Size"] for row in self.__data if "Size" in row]
        return median(sizes) if sizes else 0

    def _find_most_starred_repo(self) -> str:
        return max(self.__data, key=lambda x: x.get("Stars", 0)).get("Name", "N\A")

    def _find_repos_without_language(self) -> list[str]:
        return [row.get("Name", "N/A") for row in self.__data if not row.get("Language")]

    def _find_top_10_by_commits(self) -> list[str]:
        sorted_by_commits = sorted(self.__data, key=lambda x: x.get("Commits", 0), reverse=True)  # В файле нет коммитов
        sorted_by_commits = sorted_by_commits[:10]
        return [row.get("Name", "N/A") for row in sorted_by_commits]

    def _calculate_language_distribution(self) -> dict:
        counts = defaultdict(int)
        for row in self.__data:
            lang = row.get("Language", "Undefined")
            counts[lang] += 1
        return dict(counts)
