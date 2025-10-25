from homework_oop.CSVReader import CSVReader
from typing import List, Dict, Any
from enum import Enum
from difflib import get_close_matches


class OperationType(Enum):
    SELECT = 1
    SORT = 2
    GROUP = 3

class DataProcessor():
    def __init__(self, data: CSVReader):
        self.data = data
        self._operations: List[tuple] = []
        self._executed: bool = False
        self._result: Any = None

    def select(self, *columns: str) -> 'DataProcessor':
        self._operations.append((OperationType.SELECT, columns))
        self.executed = False

        return self

    def sort_by(self, column: str, reverse: bool = False) -> 'DataProcessor':
        self._operations.append((OperationType.SORT, (column, reverse)))
        self.executed = False

        return self

    def group_by(self, column: str) -> 'DataProcessor':
        self._operations.append((OperationType.GROUP, column))
        self.executed = False

        return self

    def _validate_column(self, column: str) -> None:
        available_column_names = self.data.get_column_names()

        if column not in available_column_names:
            close_matches = get_close_matches(
                column, available_column_names, n=3, cutoff=0.6)

            error_msg = f"Столбец {column} не найден.\nДоступные столбцы {available_column_names}"
            if close_matches:
                error_msg += f"\n\nВероятно подойдёт следуюущий"
                for close_match in close_matches:
                    error_msg += f"\n{close_match}"
            raise ValueError(error_msg)

    def _validate_columns(self, columns: tuple) -> None:
        available_column_names = self.data.get_column_names()
        invalid_columns = [
            col for col in columns if col not in available_column_names]

        if invalid_columns:
            error_msg = f"Столбцы не найдены: {', '.join(invalid_columns)}\nДоступные столбцы: {', '.join(available_column_names)}"

            for invalid_col in invalid_columns:
                close_matches = get_close_matches(
                    invalid_col, available_column_names, n=2, cutoff=0.6)
                if close_matches:
                    error_msg += f"\n\nДля '{invalid_col}' возможно подойдёт: {', '.join(close_matches)}"

            raise ValueError(error_msg)

    def _optimize_operations(self) -> List[tuple]:
        if not self._operations:
            return []

        selects = [op for op in self._operations if op[0]
                   == OperationType.SELECT]
        sorts = [op for op in self._operations if op[0] == OperationType.SORT]
        groups = [op for op in self._operations if op[0]
                  == OperationType.GROUP]

        optimezed = []
        optimezed.extend(sorts)
        optimezed.extend(selects)
        optimezed.extend(groups)

        return optimezed

    def _apply_select(self, data: List[Dict[str, str]], columns: tuple) -> List[Dict[str, str]]:
        self._validate_columns(columns)

        return [{col: row.get(col, '') for col in columns} for row in data]

    def _apply_sort(self, data: List[Dict[str, str]], params: tuple) -> List[Dict[str, str]]:
        column, reverse = params
        self._validate_column(column)
        
        try:
            def sort_key(row):
                value = row.get(column, '')
                if value is None:
                    return ''
                return str(value)
            
            return sorted(data, key=sort_key, reverse=reverse)
        except Exception as e:
            raise ValueError(f"Ошибка при сортировке по столбцу '{column}': {str(e)}")

    def _apply_group(self, data: List[Dict[str, str]], column: str) -> Dict[str, List[Dict[str, str]]]:
        self._validate_column(column)
        
        groups: Dict[str, List[Dict[str, str]]] = {}
        for row in data:
            key = row.get(column, '')
            if key not in groups:
                groups[key] = []
            groups[key].append(row)
            
        return groups
    
    def execute(self) -> Any:
        if self._executed:
            return self._result
        
        data = self.data.get_all_data()
        
        if not data:
            self._result = [] if not any(op[0] == OperationType.GROUP for op in self._operations) else {}
            self._executed = True
            return self._result
        
        optimized_operations = self._optimize_operations()

        result = data
        for op_type, params in optimized_operations:
            if (op_type == OperationType.SELECT):
                result = self._apply_select(result, params)
            elif (op_type == OperationType.GROUP):
                result = self._apply_group(result, params)
            elif (op_type == OperationType.SORT):
                result = self._apply_sort(result, params)
                
        self._result = result
        self._executed = True
        
        return self._result
    
    def reset(self) -> 'DataProcessor':
        self._operations = []
        self._result = None
        self._executed = False
        return self 