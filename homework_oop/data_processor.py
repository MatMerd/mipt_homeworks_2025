from __future__ import annotations
from typing import List, Dict, Any, Optional, Union, Callable
from collections import defaultdict
import operator
import difflib


class DataProcessor:
    def __init__(self, data: List[Dict[str, Any]]):
        """
        :param data: Данные для обработки
        """
        self._original_data = data
        self._data = data.copy()
        self._operations = []
        self._executed = False
        self._field_info = self._analyze_fields()

    def _analyze_fields(self) -> Dict[str, Any]:
        """Анализ полей данных"""
        if not self._original_data:
            return {}

        field_info = {}
        for field in self._original_data[0].keys():
            # Определяем тип данных поля
            sample_value = self._original_data[0].get(field)
            field_type = type(sample_value).__name__ if sample_value is not None else 'unknown'

            # Собираем уникальные значения для подсказок
            unique_values = set()
            for row in self._original_data[:100]:  # Ограничиваем для производительности
                if field in row:
                    unique_values.add(str(row[field]))

            field_info[field] = {
                'type': field_type,
                'sample_values': list(unique_values)[:5]  # Первые 5 значений для подсказок
            }

        return field_info

    def _suggest_fields(self, field: str) -> List[str]:
        """
        Предлагает похожие по написанию атрибуты таблицы
        :param field: атрибут
        :return: предполагаемые атрибуты
        """
        available_fields = list(self._field_info.keys())
        suggestions = difflib.get_close_matches(field, available_fields, n=3, cutoff=0.6)
        return suggestions

    def _validate_field(self, field: str):
        """
        Проверяет атрибут на существование
        :param field: атрибут
        :return:
        """
        if not self._original_data:
            return

        if field not in self._original_data[0]:
            raise ValueError(
                f"Атрибут '{field}' не найден"
            )

    def select(self, fields: List[str]) -> DataProcessor:
        """
        Выбирает из таблицы данные определенных атрибутов
        :param fields: Атрибуты таблицы
        :return:
        """
        for field in fields:
            self._validate_field(field)

        self._operations.append(('select', {'fields': fields}))
        return self

    def where(self, condition: Callable[[Dict[str, Any]], bool]) -> DataProcessor:
        """
        Фильтрует данные по условию
        :param condition: условие
        :return:
        """
        self._operations.append(('where', {'condition': condition}))
        return self

    def order_by(self, field: str, descending: bool = False) -> DataProcessor:
        """
        Сортирует данные по атрибуту
        :param field: атрибут
        :param descending: порядок
        :return:
        """
        self._validate_field(field)
        self._operations.append(('order_by', {'field': field, 'descending': descending}))
        return self

    def group_by(self, field: str, aggregation: Dict[str, Callable] = None) -> DataProcessor:
        """
        Группирует данные из таблицы
        :param field: поле для группировки
        :param aggregation: словарь с агрегационными функциями {'новое_поле': функция}
        """
        self._validate_field(field)

        if aggregation is None:
            aggregation = {}

        for agg_field in aggregation.keys():
            if agg_field in self._field_info:
                raise ValueError(
                    f"Агрегационное поле '{agg_field}' конфликтует с существующим полем. "
                    f"Используйте другое имя."
                )

        self._operations.append(('group_by', {'field': field, 'aggregation': aggregation}))
        return self

    def limit(self, count: int) -> DataProcessor:
        """
        Ограничивает количество возвращаемых данных
        :param count: максимальное количество
        :return:
        """
        if count < 0:
            raise ValueError("Лимит не может быть отрицательным")

        self._operations.append(('limit', {'count': count}))
        return self

    def _optimize_operations_order(self) -> List[tuple]:
        """
        Оптимизирует порядок выполнения операций для более быстрого выполнения
        :return:
        """
        if not self._operations:
            return []

        where_ops = []
        select_ops = []
        order_by_ops = []
        group_by_ops = []
        limit_ops = []

        for operation in self._operations:
            op_type, params = operation

            if op_type == 'where':
                where_ops.append(operation)
            elif op_type == 'select':
                select_ops.append(operation)
            elif op_type == 'order_by':
                order_by_ops.append(operation)
            elif op_type == 'group_by':
                group_by_ops.append(operation)
            elif op_type == 'limit':
                limit_ops.append(operation)

        # Оптимальный порядок: where -> group_by -> order_by -> select -> limit
        optimized_order = []

        optimized_order.extend(where_ops)
        optimized_order.extend(group_by_ops)
        optimized_order.extend(order_by_ops)
        optimized_order.extend(select_ops)
        optimized_order.extend(limit_ops)

        return optimized_order

    def _execute_where(self, data: List[Dict[str, Any]], condition: Callable) -> List[Dict[str, Any]]:
        """
        Выополняет фильтрацию данных
        :param data: данные
        :param condition: функция проверки записи
        :return:
        """
        return [row for row in data if condition(row)]

    def _execute_select(self, data: List[Dict[str, Any]], fields: List[str]) -> List[Dict[str, Any]]:
        """
        Выполняет селект данных
        :param data: данные
        :param fields: атрибуты
        :return:
        """
        return [{field: row[field] for field in fields if field in row} for row in data]

    def _execute_order_by(self, data: List[Dict[str, Any]], field: str, descending: bool = False) -> List[Dict[str, Any]]:
        """
        Выполняет сортировку данных
        :param data: данные
        :param field: атрибут
        :param descending: порядок сортировки
        :return:
        """

        def get_sort_key(row):
            value = row.get(field)
            return (value is not None, value) if not descending else (value is None, value)

        return sorted(data, key=get_sort_key, reverse=descending)

    def _get_sort_key(self, row, field, descending):
            value = row.get(field)
            return (value is not None, value) if not descending else (value is None, value)

    def _execute_group_by(self, data: List[Dict[str, Any]], field: str, aggregation: Dict[str, Callable]) -> List[
        Dict[str, Any]]:
        """
        Выполняет группировку данных
        :param data: данные
        :param field: атрибут группировки
        :param aggregation: набор полей с их агрегирующими функциями
        :return:
        """
        # Создаем обычный словарь для группировки
        groups = {}

        # Группируем данные
        for row in data:
            group_key = row.get(field)

            # Если ключа еще нет в словаре, создаем пустой список
            if group_key not in groups:
                groups[group_key] = []

            # Добавляем строку в соответствующую группу
            groups[group_key].append(row)

        # Применяем агрегации
        result = []
        for group_key, group_data in groups.items():
            group_row = {field: group_key}

            for agg_name, agg_func in aggregation.items():
                try:
                    # Для агрегации используем все числовые поля кроме группировочного
                    values_to_aggregate = []
                    for row in group_data:
                        for key, value in row.items():
                            if key != field and isinstance(value, (int, float)):
                                values_to_aggregate.append(value)

                    if values_to_aggregate:
                        group_row[agg_name] = agg_func(values_to_aggregate)
                    else:
                        group_row[agg_name] = None
                except Exception as e:
                    raise ValueError(f"Ошибка в агрегационной функции {agg_name}: {e}")

            result.append(group_row)

        return result

    def _execute_limit(self, data: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """
        Выполняет ограничение выборки
        :param data: данные
        :param count: максимальное количество
        :return:
        """
        return data[:count]

    def execute(self) -> List[Dict[str, Any]]:
        """
        Выполняет список операций в оптимальном порядке
        :return: Данные, удовлетворяющие запросу
        """
        if self._executed:
            return self._data

        if not self._operations:
            return self._original_data

        # Оптимизируем порядок операций
        optimized_operations = self._optimize_operations_order()

        # Выполняем операции
        result = self._original_data.copy()

        for operation_type, params in optimized_operations:
            try:
                if operation_type == 'where':
                    result = self._execute_where(result, params['condition'])
                elif operation_type == 'select':
                    result = self._execute_select(result, params['fields'])
                elif operation_type == 'order_by':
                    result = self._execute_order_by(result, params['field'], params['descending'])
                elif operation_type == 'group_by':
                    result = self._execute_group_by(result, params['field'], params['aggregation'])
                elif operation_type == 'limit':
                    result = self._execute_limit(result, params['count'])
            except Exception as e:
                raise RuntimeError(f"Ошибка при выполнении операции {operation_type}: {e}")

        self._data = result
        self._executed = True
        return result
