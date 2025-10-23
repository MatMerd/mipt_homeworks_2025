from typing import List, Dict, Any, Optional, Union
from difflib import get_close_matches


class DataHandler:
    def __init__(self, reader: Any) -> None:
        self.result: Optional[Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]] = None
        self.reader = reader
        self.operations: List[tuple] = []

    def _validate_field(self, field: str) -> None:
        if field not in self.reader.fieldnames:
            closest = get_close_matches(field, self.reader.fieldnames, n=3)
            error_msg = f"Поле '{field}' не найдено."
            if closest:
                error_msg += f" Возможно вы имели в виду: {', '.join(closest)}"
            raise ValueError(error_msg)

    def select(self, fields: Optional[List[str]] = None) -> 'DataHandler':
        if fields:
            for field in fields:
                self._validate_field(field)
            self.operations.append(('select', fields))
        return self

    def sort(self, field: str, reverse: bool = False) -> 'DataHandler':
        self._validate_field(field)
        self.operations.append(('sort', field, reverse))
        return self

    def filter(self, field: str, value: Any) -> 'DataHandler':
        self._validate_field(field)
        self.operations.append(('filter', field, value))
        return self

    def group_by(self, field: str) -> 'DataHandler':
        self._validate_field(field)
        self.operations.append(('group_by', field))
        return self

    def execute(self) -> Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
        appreciate_sort = ['filter', 'sort', 'group_by', 'select']
        optimized_way = sorted(self.operations, key=lambda row: appreciate_sort.index(row[0]))
        result: Union[
            List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]] = self.reader.reader.copy()

        for operation in optimized_way:
            op_type = operation[0]

            if op_type == 'filter':
                field, value = operation[1], operation[2]
                result = [item for item in result if item.get(field) == value]

            elif op_type == 'sort':
                field, reverse = operation[1], operation[2]
                result = sorted(result, key=lambda x: x.get(field, ''), reverse=reverse)

            elif op_type == 'group_by':
                field = operation[1]
                grouped: Dict[str, List[Dict[str, Any]]] = {}
                for item in result:
                    key = item.get(field, '')
                    if key not in grouped:
                        grouped[key] = []
                    grouped[key].append(item)
                result = grouped

            elif op_type == 'select':
                fields = operation[1]
                if isinstance(result, dict):
                    for key in result:
                        result[key] = [{f: item.get(f) for f in fields} for item in result[key]]
                else:
                    result = [{f: item.get(f) for f in fields} for item in result]

        self.result = result
        return result