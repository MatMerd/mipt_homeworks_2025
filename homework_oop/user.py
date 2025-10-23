from typing import Any, Dict, List
from homework_oop.state import State
from homework_oop.reader import Reader


class User:
    def __init__(self, status: str = "active") -> None:
        self.status = status
        self.saved_queries: Dict[str, Dict[str, Any]] = {}

    def save_query(self, name: str, state: State) -> None:
        self.saved_queries[name] = {
            'operations': state.operations.copy(),
            'result': state.result
        }

    def execute_saved_query(self, name: str, reader: Reader) -> List[Dict[str, Any]]:
        if name not in self.saved_queries:
            raise ValueError(f"Запрос '{name}' не найден")

        saved_query = self.saved_queries[name]
        state = State(reader)
        state.operations = saved_query['operations'].copy()
        return state.execute()