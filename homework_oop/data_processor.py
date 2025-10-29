from dataclasses import dataclass
import difflib
from typing import List, Dict, Any, Union, Callable
from collections import defaultdict

class DataProcessor:
    """
    Класс для выбора, сортировки и группировки данных
    с оптимизацией порядка операций

    Fields:
        original_data - исходные данные файла
        data - копия данных для обработки
        operations - список операций
        available_fields - доступные для операций поля
    """

    def __init__(self, data: List[Dict[str, Any]]):
        """
        Args:
            data - исходные данные файла
        """

        self.original_data = data
        self.data = data.copy()
        self.operations = []
        self.available_fields = self._get_available_fields()

    def _get_available_fields(self) -> List[str]:
        """
        Получение списка всех полей
        """

        if not self.original_data:
            return []
        return list(self.original_data[0].keys())

    def _validate_field(self, field: str, operation: str) -> str:
        """
        Проверка поля с подсказками по похожим полям

        Args:
            field: поле для проверки
            operation: название операции для сообщения об ошибке
        Returns:
            Проверенное поле (если найдено)
        Raises:
            ValueError: если поле не найдено
        """

        if field in self.available_fields:
            return field

        similar_fields = difflib.get_close_matches(field, self.available_fields, n=3, cutoff=0.3)

        error_msg = f"Поле '{field}' не найдено в операции {operation}."
        if similar_fields:
            error_msg += f" Возможно, вы имели в виду: {', '.join(similar_fields)}"
        else:
            error_msg += f" Доступные поля: {', '.join(self.available_fields)}"

        raise ValueError(error_msg)

    def select(self, fields: Union[str, List[str]]) -> 'DataProcessor':
        """
        Выбор определенных полей

        Args:
            fields: поле или список полей для выборки
        """

        if isinstance(fields, str):
            fields = [fields]

        for field in fields:
            self._validate_field(field, "select")

        self.operations.append(('select', fields))
        return self

    def where(self, condition: Callable[[Dict[str, Any]], bool]) -> 'DataProcessor':
        """
        Фильтрация данных по условию

        Args:
            condition: функция-условие для фильтрации
        """

        self.operations.append(('where', condition))
        return self

    def sort_by(self, field: str, reverse: bool = False) -> 'DataProcessor':
        """
        Сортировка данных по полю

        Args:
            field: поле для сортировки
            reverse: обратный порядок сортировки
        """

        self._validate_field(field, "sort_by")
        self.operations.append(('sort_by', (field, reverse)))
        return self

    def group_by(self, field: str) -> 'DataProcessor':
        """
        Группировка данных по полю

        Args:
            field: поле для группировки
        """

        self._validate_field(field, "group_by")
        self.operations.append(('group_by', field))
        return self

    def limit(self, count: int) -> 'DataProcessor':
        """
        Ограничение количества результатов

        Args:
            count: максимальное количество записей
        Raises:
            ValueError: в случае отрицательного ограничения
        """

        if count < 0:
            raise ValueError(f"Ограничение не может быть отрицательным: {count}")

        self.operations.append(('limit', count))
        return self

    def _optimize_operations(self) -> List:
        """
        Оптимизация порядка операций для лучшей производительности
        (where -> sort_by -> group_by -> select -> limit)

        Returns:
            Оптимизированный список операций
        """

        if not self.operations:
            return []

        operations_by_type = defaultdict(list)
        for op in self.operations:
            operations_by_type[op[0]].append(op)

        optimized_ops = []

        optimized_ops.extend(operations_by_type['where'])
        optimized_ops.extend(operations_by_type['sort_by'])
        optimized_ops.extend(operations_by_type['group_by'])
        optimized_ops.extend(operations_by_type['select'])
        optimized_ops.extend(operations_by_type['limit'])

        return optimized_ops

    def _apply_operation(self, data: List[Dict[str, Any]], operation: tuple) -> Any:
        """
        Применение одной операции к данным

        Args:
            data: входные данные
            operation: операция для применения
        Returns:
            Результат применения операции
        """

        op_type, op_value = operation

        if op_type == 'select':
            fields = op_value
            return [{field: item.get(field) for field in fields} for item in data]

        elif op_type == 'where':
            condition = op_value
            return [item for item in data if condition(item)]

        elif op_type == 'sort_by':
            field, reverse = op_value
            return sorted(data,
                         key=lambda x: (x.get(field) is not None, x.get(field)),
                         reverse=reverse)

        elif op_type == 'group_by':
            field = op_value
            grouped = defaultdict(list)
            for item in data:
                key = item.get(field)
                grouped[key].append(item)
            return dict(grouped)

        elif op_type == 'limit':
            count = op_value
            return data[:count]

        return data

    def execute(self) -> Union[List[Dict[str, Any]], Dict[Any, List[Dict[str, Any]]]]:
        """
        Выполнение всех операций в оптимальном порядке

        Returns:
            Результат обработки данных
        """

        if not self.operations:
            return self.data.copy()

        optimized_ops = self._optimize_operations()
        result = self.original_data.copy()

        for operation in optimized_ops:
            try:
                result = self._apply_operation(result, operation)
            except Exception as e:
                op_type, op_value = operation
                raise RuntimeError(f"Ошибка при выполнении операции {op_type} с параметрами {op_value}: {e}")

        return result

    def reset(self) -> 'DataProcessor':
        """
        Сброс всех операций
        """

        self.operations = []
        self.data = self.original_data.copy()
        return self