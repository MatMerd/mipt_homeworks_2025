from typing import Any, List, Optional, Dict
from .models import SortOrder


class UserSession:    
    def __init__(self, username: str):
        self.username = username
        self._saved_queries: Dict[str, Dict[str, Any]] = {}
        self._current_sort_config: Optional[Dict[str, Any]] = None
        self._current_group_config: Optional[Dict[str, Any]] = None
    
    def save_sort_config(self, name: str, sort_key: str, 
                        order: SortOrder = SortOrder.ASCENDING) -> None:
        self._current_sort_config = {
            'name': name,
            'sort_key': sort_key,
            'order': order
        }
        print(f"Сохранена конфигурация сортировки '{name}': {sort_key}")
    
    def save_group_config(self, name: str, group_key: str) -> None:
        self._current_group_config = {
            'name': name,
            'group_key': group_key
        }
        print(f"Сохранена конфигурация группировки '{name}': {group_key}")
    
    def save_query(self, query_name: str, 
                  filters: Optional[List[str]] = None,
                  sort_config_name: Optional[str] = None,
                  group_config_name: Optional[str] = None) -> None:
        query_config = {
            'filters': filters or [],
            'sort_config': self._current_sort_config if sort_config_name else None,
            'group_config': self._current_group_config if group_config_name else None
        }
        self._saved_queries[query_name] = query_config
        print(f"Запрос '{query_name}' сохранён")
    
    def get_saved_queries(self) -> List[str]:
        return list(self._saved_queries.keys())