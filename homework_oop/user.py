from __future__ import annotations
from typing import List, Dict, Any, Callable, Optional

from data_processor import DataProcessor
from query import Query


class User:
    def __init__(self, data: List[Dict[str, Any]]):
        self._data = data
        self._query = Query()
        self._processor = DataProcessor(data)

    def apply_saved_settings(self) -> User:
        """
        Применяет пользовательские настройки
        :return:
        """
        settings = self._query.get_settings()

        if settings["sort_field"]:
            self._processor.order_by(
                settings["sort_field"], settings["sort_descending"]
            )

        if settings["group_field"]:
            self._processor.group_by(settings["group_field"], settings["aggregation"])

        return self

    def execute_saved_query(self, query_id: str) -> List[Dict[str, Any]]:
        """
        Выполняет запрос по id
        :param query_id: id запроса
        :return: данные, удовлетворяющие запросу
        """
        saved_query = self._query.get_query(query_id)
        if not saved_query:
            raise ValueError(f"Запрос с ID {query_id} не найден")

        new_processor = DataProcessor(self._data)

        for op_type, params in saved_query["operations"]:
            if op_type == "select":
                new_processor.select(params["fields"])
            elif op_type == "where":
                new_processor.where(params["condition"])
            elif op_type == "order_by":
                new_processor.order_by(params["field"], params["descending"])
            elif op_type == "group_by":
                new_processor.group_by(params["field"], params["aggregation"])
            elif op_type == "limit":
                new_processor.limit(params["count"])

        return new_processor.execute()

    def create_and_save_query(self, name: str, operations: List[tuple]) -> str:
        """
        Создает и сохраняет кастомный запрос
        :param name: название запроса
        :param operations: операции
        :return:
        """
        return self._query.save_query(name, operations)

    def get_saved_queries(self) -> List[Dict[str, Any]]:
        """
        Возвращает список сохраненных запросов
        :return:
        """
        return self._query.list_queries()

    def update_user_settings(
        self,
        sort_field: Optional[str] = None,
        sort_descending: bool = False,
        group_field: Optional[str] = None,
        aggregation: Optional[Dict[str, Callable]] = None,
    ):
        """
        Обновляет настройки пользователя
        :param sort_field: атрибут сортировки
        :param sort_descending: порядок сортировки
        :param group_field: атрибут группировки
        :param aggregation: функции агрегации
        :return:
        """
        self._query.save_settings(sort_field, sort_descending, group_field, aggregation)

    def get_default_query(self):
        """
        Возвращает результат для дефолтного запроса, основываясь на настройках пользователя
        :return:
        """
        settings = self._query.get_settings()
        print(settings)
        if not settings["group_field"]:
            self._processor.select(["Name", "URL", "Size"])
        return self._processor.limit(100).execute()
