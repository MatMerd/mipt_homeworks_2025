from typing import List, Dict, Any, Optional
import statistics


class StatCollector:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def get_median_repo_size(self) -> Optional[float]:
        """
        Возвращает медиану по размеру репозитория
        :return:
        """
        sizes = []

        for repo in self.data:
            size = repo.get("Size")
            if size is not None:
                sizes.append(int(size))

        if not sizes:
            return None

        try:
            return statistics.median(sizes)
        except statistics.StatisticsError:
            return None

    def get_most_starred_repo(self) -> Optional[Dict[str, Any]]:
        """
        Возвращает максимально залайканный репозиторий
        :return:
        """
        if not self.data:
            return None

        max_stars = -1
        most_starred = None

        for repo in self.data:
            stars = repo.get("Stars")
            # print(stars)
            if stars and int(stars) > max_stars:
                max_stars = int(stars)
                most_starred = repo

        return most_starred

    def get_percentage_of_repos_without_language(self) -> float:
        """
        Возвращает процент репозиториев без языка
        :return:
        """
        repos_without_lang = []

        for repo in self.data:
            language = repo.get("Language")
            if not language or language in ["", "<null>", "null", "None", None]:
                repos_without_lang.append(repo)

        return len(repos_without_lang) / len(self.data)

    # def get_top10_repos_by_commits(self) -> List[Dict[str, Any]]:
    #     """
    #     Возвращает топ10 репозиториев с самым большим числом коммитов
    #     :return:
    #     """
    #     if not self.data:
    #         return []
    #
    #     repos_with_commits = []
    #
    #     for repo in self.data:
    #         commits = repo.get('commits')

    def get_avg_issues_count(self) -> Optional[float]:
        """
        Возвращает среднее число issues в репозиториях
        """
        issues_list = []

        for repo in self.data:
            issues = repo.get("Issues")

            if isinstance(issues, str):
                issues_list.append(int(issues))

        if not issues_list:
            return None

        return sum(issues_list) / len(issues_list)

    def get_all_statistics(self) -> Dict[str, Any]:
        """
        Возвращает полную статистику по репозиторииям
        :return:
        """
        return {
            "median_repo_size": self.get_median_repo_size(),
            "most_starred_repo": self.get_most_starred_repo(),
            "avg_issues_count": self.get_avg_issues_count(),
            "get_percentage_of_repos_without_language": self.get_percentage_of_repos_without_language(),
        }
