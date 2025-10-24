from collections import defaultdict


class DataProcessor:
    __slots__ = ("__available_fields", "__data", "__operations")

    def __init__(self, data: list[dict]) -> None:
        self.__available_fields: list[str] = list(data[0].keys()) if data else []
        self.__data: list[dict] = data
        self.__operations: list[tuple] = []

    @staticmethod
    def __validate_fields(fields: list[str], available_fields: list[str]) -> None:
        invalid_fields = [f for f in fields if f not in available_fields]
        if invalid_fields:
            error_message = f"Ошибка: не найдены поля: {", ".join(invalid_fields)}."
            raise ValueError(error_message)

    def select(self, *fields: str):
        self.__validate_fields(list(fields), self.__available_fields)
        self.__operations.append(("select", fields))
        return self

    def sort_by(self, field: str, reverse: bool = False):
        self.__validate_fields([field], self.__available_fields)
        self.__operations.append(("sort_by", (field, reverse)))
        return self

    def group_by(self, field: str):
        self.__validate_fields([field], self.__available_fields)
        self.__operations.append(("group_by", field))
        return self

    def execute(self) -> list[dict] | dict:
        """
        Выполняет все добавленные операции в оптимальном порядке.
        Оптимальный порядок: select -> sort -> group.
        1. select: Уменьшает объем данных для последующих операций.
        2. sort_by: Сортировка эффективнее на уже уменьшенном наборе данных.
        3. group_by: Группировка является финальной агрегирующей операцией.
        """
        processed_data: list[dict] = self.__data.copy()
        is_grouped: bool = False
        fields: list[str] = self.__available_fields

        execution_order = {"select": [], "sort_by": [], "group_by": []}
        for op_type, op_args in self.__operations:
            if is_grouped:
                if op_type == "select" or op_type == "sort_by":
                    raise AttributeError("Ошибка: Нельзя вызывать 'select' и 'sort_by' после 'group_by'.")
                if op_type == 'group_by':
                    raise AttributeError("Ошибка: Двойная группировка не поддерживается.")
            if op_type == "group_by":
                is_grouped = True
            if op_type == "select":
                try:
                    self.__validate_fields(op_args, fields)
                    fields = list(set(op_args))
                except ValueError:
                    raise AttributeError("Ошибка: Неподдерживаемый порядок запросов 'select'")
            execution_order[op_type].append(op_args)

        if execution_order['select']:
            selected_fields = execution_order['select'][-1]
            processed_data = [
                {field: row.get(field, None) for field in selected_fields}
                for row in processed_data
            ]

        for field, reverse in execution_order["sort_by"]:
            processed_data.sort(key=lambda row: row.get(field, 0), reverse=reverse)

        if execution_order["group_by"]:
            field = execution_order["group_by"][0]
            grouped_data = defaultdict(list)
            for row in processed_data:
                key = row.get(field, "N/A")
                grouped_data[key].append(row)
            return dict(grouped_data)

        return processed_data
