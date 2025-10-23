import typing as tp
from datetime import datetime

Repo: tp.TypeAlias = tp.Dict[str, str]
RepoList: tp.TypeAlias = tp.List[tp.Dict[str, str]]

class DataStatistics:
    """
    Класс для вычисления различных статистик по данным репозиториев.
    """
    @staticmethod
    def median_repo_size(data: RepoList) -> float:
        median = 0.0
        for repo in data:
            median += float(repo["Size"])
        return median / len(data)
    
    @staticmethod
    def max_stars_repo(data: RepoList) -> Repo:
        max_stars = int(data[0]["Stars"])
        max_stars_repo = data[0]
        for repo in data:
            if int(repo["Stars"]) > max_stars:
                max_stars = int(repo["Stars"])
                max_stars_repo = repo
        return max_stars_repo

    @staticmethod
    def repos_without_language(data: RepoList) -> RepoList:
        return [repo for repo in data if repo["Language"] == '']
    
    @staticmethod
    def top_recently_updated(data: RepoList, top_n: int = 10) -> RepoList:
        sorted_repos = sorted(
            data,
            key=lambda r: datetime.fromisoformat(r["Updated At"]),
            reverse=True
        )
        return sorted_repos[:top_n]
    
    @staticmethod
    def top_active_repos(data: RepoList, top_n: int = 10) -> RepoList:
        sorted_repos = sorted(
            data,
            key=lambda r: (int(r["Issues"]) + int(r["Forks"]) + int(r["Stars"]), datetime.fromisoformat(r["Updated At"])),
            reverse=True
        )
        return sorted_repos[:top_n]
