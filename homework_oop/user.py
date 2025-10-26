from dataclasses import dataclass, field
from datetime import datetime

from homework_oop.logger import log_operation
from query_executor import QueryExecutor


@dataclass
class SavedQuery:
    name: str
    description: str
    operations: list
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def operation_types(self):
        return [type(op).__name__ for op in self.operations]

    @property
    def is_complex(self):
        return len(self.operations) > 2


class User:
    def __init__(self, name):
        self.name = name
        self._saved_queries = {}

    @property
    def saved_query_names(self):
        return list(self._saved_queries.keys())

    @property
    def total_saved_queries(self):
        return len(self._saved_queries)

    @property
    def complex_queries(self):
        return [query for query in self._saved_queries.values() if query.is_complex]

    @log_operation
    def save_query(self, name, executor):
        self._saved_queries[name] = SavedQuery(
            name=name,
            description=f"Сохраненный запрос пользователя {self.name}",
            operations=executor.operations.copy()
        )

    @log_operation
    def execute_saved_query(self, name, data):
        if name not in self._saved_queries:
            raise KeyError(f"Запрос '{name}' не найден")

        saved_query = self._saved_queries[name]
        executor = QueryExecutor(data)
        executor.operations = saved_query.operations.copy()

        return executor.execute()