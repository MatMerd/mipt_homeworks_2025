from typing import List, Dict, Any, Optional, Callable
import json
import uuid
from datetime import datetime

class Query:
    def __init__(self):
        self.saved_queries = {}
        self.default_settings = {
            'sort_field': None,
            'sort_descending': False,
            'group_field': None,
            'aggregation': None
        }

    def save_query(self, name: str, query_operations: List[tuple]) -> str:
        """
        Сохраняет запрос
        :param name: название запроса (тег)
        :param query_operations: операции в запросе
        :return:
        """
        query_id = str(uuid.uuid4())

        self.saved_queries[query_id] = {
            'id': query_id,
            'name': name,
            'operations': query_operations
        }

        return query_id

    def get_query(self, query_id: str) -> Optional[Dict[str, Any]]:
        """
        Возвращает запрос по id
        :param query_id:
        :return:
        """
        return self.saved_queries.get(query_id)

    def list_queries(self) -> List[Dict[str, Any]]:
        """
        Возвращает все запросы
        :return:
        """
        return list(self.saved_queries.values())

    def delete_query(self, query_id: str) -> bool:
        """
        Удаляет запрос по id
        :param query_id:
        :return:
        """
        if query_id in self.saved_queries:
            del self.saved_queries[query_id]
            return True
        return False

    def update_query(self, query_id: str, name: str = None, operations: List[tuple] = None) -> bool:
        """
        Обновляет запрос по id
        :param query_id: id запроса
        :param name: название запроса
        :param operations: операции
        :return:
        """
        if query_id not in self.saved_queries:
            return False

        if name is not None:
            self.saved_queries[query_id]['name'] = name

        if operations is not None:
            self.saved_queries[query_id]['operations'] = operations

        return True

    def save_settings(self, sort_field: str = None, sort_descending: bool = False,
                      group_field: str = None, aggregation: Dict[str, Callable] = None):
        """
        Сохраняет пользовательские настройки
        :param sort_field: атрибут сортировки
        :param sort_descending: порядок
        :param group_field: атрибут группировки
        :param aggregation: агрегационные функции
        :return:
        """
        self.default_settings.update({
            'sort_field': sort_field,
            'sort_descending': sort_descending,
            'group_field': group_field,
            'aggregation': aggregation
        })

    def get_settings(self) -> Dict[str, Any]:
        """
        Возвращает пользовательские настройки
        :return:
        """
        return self.default_settings.copy()