from homework_oop.logger import log_operation


class FieldNotFoundError(Exception):
    def __init__(self, field, available_fields):
        self.field = field
        self.available_fields = available_fields
        super().__init__(
            f"Поле '{field}' не найдено. Доступные поля: {available_fields}"
        )


class FilterOperation:
    def __init__(self, condition):
        self.condition = condition

    @log_operation
    def execute(self, data):
        return [item for item in data if self.condition(item)]


class SortOperation:
    def __init__(self, key, reverse=False):
        self.key = key
        self.reverse = reverse

    @log_operation
    def execute(self, data):
        if not data:
            return data

        if not hasattr(data[0], self.key):
            available_fields = [attr for attr in dir(data[0])
                                if not attr.startswith('_') and not callable(getattr(data[0], attr))]
            raise FieldNotFoundError(self.key, available_fields)

        return sorted(data, key=lambda x: getattr(x, self.key, 0), reverse=self.reverse)


class GroupByOperation:
    def __init__(self, key):
        self.key = key

    @log_operation
    def execute(self, data):
        if not data:
            return data

        if not hasattr(data[0], self.key):
            available_fields = [attr for attr in dir(data[0])
                                if not attr.startswith('_') and not callable(getattr(data[0], attr))]
            raise FieldNotFoundError(self.key, available_fields)

        groups = {}
        for item in data:
            group_key = getattr(item, self.key)
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(item)

        return [{'group_key': key, 'items': items} for key, items in groups.items()]


class QueryExecutor:
    def __init__(self, data):
        self.data = data
        self.operations = []

    @log_operation
    def filter(self, condition):
        self.operations.append(FilterOperation(condition))
        return self

    @log_operation
    def sort(self, key, reverse=False):
        self.operations.append(SortOperation(key, reverse))
        return self

    @log_operation
    def group_by(self, key):
        self.operations.append(GroupByOperation(key))
        return self

    def _optimize_operations(self):
        filters = [op for op in self.operations if isinstance(op, FilterOperation)]
        sorts = [op for op in self.operations if isinstance(op, SortOperation)]
        groups = [op for op in self.operations if isinstance(op, GroupByOperation)]
        return filters + sorts + groups

    @log_operation
    def execute(self):
        if not self.operations:
            return self.data

        optimized_ops = self._optimize_operations()
        result = self.data

        for operation in optimized_ops:
            result = operation.execute(result)

        return result
