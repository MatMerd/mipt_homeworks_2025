from typing import Dict, List, Any, Optional, Callable
from .models import Repository, SortOrder


class RepositoryQueryBuilder:
    def __init__(self, repositories: List[Repository]):
        self._repositories = repositories
        self._filters: List[Callable[[Repository], bool]] = []
        self._sort_key: Optional[Callable[[Repository], Any]] = None
        self._sort_order: SortOrder = SortOrder.ASCENDING
        self._group_key: Optional[Callable[[Repository], Any]] = None
        self._result_cache: Optional[Any] = None
    
    def filter(self, condition: Callable[[Repository], bool]) -> 'RepositoryQueryBuilder':
        self._filters.append(condition)
        self._result_cache = None
        return self
    
    def sort_by(self, key: Callable[[Repository], Any], 
                order: SortOrder = SortOrder.ASCENDING) -> 'RepositoryQueryBuilder':
        self._sort_key = key
        self._sort_order = order
        self._result_cache = None
        return self
    
    def group_by(self, key: Callable[[Repository], Any]) -> 'RepositoryQueryBuilder':
        self._group_key = key
        self._result_cache = None
        return self
    
    def execute(self) -> List[Repository]:
        if self._result_cache is not None and self._group_key is None:
            return self._result_cache
        
        result = self._repositories
        for filter_func in self._filters:
            result = [repo for repo in result if filter_func(repo)]
        
        if self._sort_key:
            reverse = (self._sort_order == SortOrder.DESCENDING)
            try:
                result = sorted(result, key=self._sort_key, reverse=reverse)
            except Exception as error:
                raise ValueError(f"Ошибка при сортировке: {error}")
        
        if not self._group_key:
            self._result_cache = result
        
        return result
    
    def execute_grouped(self) -> Dict[Any, List[Repository]]:
        filtered_sorted = self.execute()
        
        if not self._group_key:
            raise ValueError("Ключ группировки не установлен")
        
        grouped: Dict[Any, List[Repository]] = {}
        for repo in filtered_sorted:
            try:
                key = self._group_key(repo)
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(repo)
            except Exception as error:
                print(f"Предупреждение: Ошибка группировки для {repo.name}: {error}")
                continue
        
        return grouped
    
    def count(self) -> int:
        return len(self.execute())
