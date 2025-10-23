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
        sizes = [float(repo['Size']) for repo in data]
        return (min(sizes) + max(sizes)) / 2
    
    @staticmethod
    def max_stars_repo(data: RepoList) -> Repo:
        return max(data, key=lambda x: int(x["Stars"]))

    @staticmethod
    def repos_without_language(data: RepoList) -> RepoList:
        return list(filter(lambda x: x["Language"] == '', data))
    
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
      
    @staticmethod
    def get_top10_most_forked(data: RepoList, top_n: int = 10) -> RepoList:
        return sorted(data, key=lambda x: int(x['Forks']), reverse=True)[:top_n]
