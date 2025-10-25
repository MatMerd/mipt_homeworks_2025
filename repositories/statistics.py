from typing import Dict, List, Any, Tuple
from .models import Repository
from collections import Counter
from statistics import median, mean

class RepositoryStatistics:    
    def __init__(self, repositories: List[Repository]):
        self.repositories = repositories
    
    def median_size(self) -> float:
        if not self.repositories:
            return 0.0
        sizes = [repo.size for repo in self.repositories]
        return median(sizes)
    
    def average_size(self) -> float:
        if not self.repositories:
            return 0.0
        sizes = [repo.size for repo in self.repositories]
        return mean(sizes)
    
    def most_starred_repositories(self, top_count: int = 10) -> List[Repository]:
        return sorted(self.repositories, 
                     key=lambda repo: repo.stars, 
                     reverse=True)[:top_count]
    
    def repositories_without_language(self) -> List[Repository]:
        return [repo for repo in self.repositories 
                if not repo.language or repo.language.strip() == '']
    
    def repositories_with_most_commits(self, top_count: int = 10) -> List[Repository]:
        return sorted(
            self.repositories,
            key=lambda repo: repo.stars + repo.forks + repo.issues,
            reverse=True
        )[:top_count]
    
    def language_distribution(self) -> Dict[str, int]:
        languages = [repo.language for repo in self.repositories if repo.language]
        return dict(Counter(languages))
    
    def top_languages(self, top_count: int = 10) -> List[Tuple[str, int]]:
        distribution = self.language_distribution()
        return sorted(distribution.items(), 
                     key=lambda item: item, 
                     reverse=True)[:top_count]
    
    def license_distribution(self) -> Dict[str, int]:
        licenses = [repo.license for repo in self.repositories if repo.license]
        return dict(Counter(licenses))
    
    def total_stars(self) -> int:
        return sum(repo.stars for repo in self.repositories)
    
    def total_forks(self) -> int:
        return sum(repo.forks for repo in self.repositories)
    
    def archived_count(self) -> int:
        return sum(1 for repo in self.repositories if repo.is_archived)
    
    def fork_count(self) -> int:
        return sum(1 for repo in self.repositories if repo.is_fork)
    
    def statistics_for_selection(self, repositories: List[Repository]) -> Dict[str, Any]:
        if not repositories:
            return {'count': 0, 'message': 'Нет репозиториев'}
        
        temp_stats = RepositoryStatistics(repositories)
        
        return {
            'total_count': len(repositories),
            'median_size': temp_stats.median_size(),
            'average_size': temp_stats.average_size(),
            'total_stars': temp_stats.total_stars(),
            'total_forks': temp_stats.total_forks(),
            'archived_count': temp_stats.archived_count(),
            'fork_count': temp_stats.fork_count(),
            'top_languages': temp_stats.top_languages(5),
            'repositories_without_language': len(temp_stats.repositories_without_language())
        }
