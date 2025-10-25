
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
import csv
import os

class User:
    _all_users: Dict[int, 'User'] = {}
    _next_id: int = 1

    def __init__(self, user_id: Optional[int] = None):
        if user_id is None:
            self.id = User._next_id
            User._next_id += 1
        else:
            self.id = user_id
            if user_id in User._all_users:
                raise ValueError(f"Пользователь с ID {user_id} уже существует.")
        self.saved_queries: Dict[str, Query] = {}
        User._all_users[self.id] = self

    @classmethod
    def get_user(cls, user_id: int) -> 'User':
        if user_id not in cls._all_users:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден.")
        return cls._all_users[user_id]

    def save_query(self, query_name: str, query: Query) -> None:
        if not isinstance(query, Query):
            raise QueryValidationError("Аргумент 'query' должен быть экземпляром класса Query.")

        if query_name in self.saved_queries:
            raise QueryValidationError(f"Запрос с именем '{query_name}' уже существует. Выберите другое имя.")

        self.saved_queries[query_name] = query
        print(f"Запрос '{query_name}' успешно сохранён для пользователя {self.id}.")

    def execute_query(self, data: List[Dict[str, Any]], query: Query) -> List[Dict[str, Any]]:
        repos_query = RepsQuery(data, query, self.id)
        result_data = repos_query.execute()
        return result_data

    def execute_saved_query(self, data: List[Dict[str, Any]], query_name: str) -> List[Dict[str, Any]]:
        if query_name not in self.saved_queries:
            raise QueryValidationError(f"Сохранённый запрос '{query_name}' не найден для пользователя {self.id}.")

        query = self.saved_queries[query_name]
        return self.execute_query(data, query)

    def list_saved_queries(self) -> List[str]:
        return list(self.saved_queries.keys())

    def delete_saved_query(self, query_name: str) -> None:
        if query_name not in self.saved_queries:
            raise QueryValidationError(f"Сохранённый запрос '{query_name}' не найден для пользователя {self.id}.")

        del self.saved_queries[query_name]
        print(f"Запрос '{query_name}' успешно удалён для пользователя {self.id}.")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, saved_queries={len(self.saved_queries)})>"
