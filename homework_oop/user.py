from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional
from enum import Enum
from datacls import Query, Operation, OperationType

class User:
    """
    Класс пользователя для сохранения запросов

    Fields:
        name - имя пользователя
        saved_queries - словарь запросов (ключ: имя запроса, значение: Query объект)
    """

    def __init__(self, name: str):
        self.name = name
        self.saved_queries: Dict[str, Query] = {}

    def add_query(self, query: Query, name: str = None) -> str:
        """
        Добавление запроса в сохраненные

        Args:
            query: объект Query
            name: имя запроса (если None - генерируется автоматически)

        Returns:
            Имя, под которым сохранен запрос
        """
        if name is None:
            name = f"query_{len(self.saved_queries) + 1}"

        self.saved_queries[name] = query
        return name
    
    def set_query_result(self, name: str, query_result):
        """
        Задаёт результат запросу
        
        Args:
            name: имя запроса
            query_result: результат запроса
        """
        self.saved_queries[name].result = query_result

    def get_query_names(self) -> List[str]:
        """
        Возвращает список всех имен сохраненных запросов
        """
        return list(self.saved_queries.keys())

    def get_query(self, name: str) -> Optional[Query]:
        """
        Получение запроса по имени

        Args:
            name: имя запроса

        Returns:
            Query объект или None, если запрос не найден
        """
        return self.saved_queries.get(name)
    
    def get_queries(self) -> Dict[str, Query]:
        """
        Получение запросов

        Returns:
            Запросы
        """
        return self.saved_queries

    def __str__(self) -> str:
        return f"User(name='{self.name}', saved_queries={len(self.saved_queries)})"


# Пример использования
if __name__ == "__main__":
    user = User("student")

    # Создаем операции
    op1 = Operation(OperationType.SELECT, ["Name", "Stars"])
    op2 = Operation(OperationType.SORT, ["Stars", True])

    op3 = Operation(OperationType.GROUP_BY, ["Language"])
    op4 = Operation(OperationType.SELECT, ["Name", "Stars"])

    # Создаем запросы
    query1 = Query(operations=[op1, op2])
    query2 = Query(operations=[op3, op4])

    # Добавляем запросы
    query1_name = user.add_query(query1)
    query2_name = user.add_query(query2, "language_query")

    # Добавляем запрос с результатом
    result_query = Query(operations=[op1, op2], result=[{"Name": "repo1", "Stars": "1000"}])
    user.add_query(result_query, "result_query")

    print(user)
    print("Имена запросов:", user.get_query_names())

    # Получаем запросы
    saved_query1 = user.get_query(query1_name)
    print(f"Запрос '{query1_name}': {len(saved_query1.operations)} операций")
    for op in saved_query1.operations:
        print(f"  - {op.operation_type.name}: {op.args}")

    saved_query2 = user.get_query("result_query")
    print(f"Результат запроса 'result_query': {saved_query2.result}")