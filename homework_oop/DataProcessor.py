from collections import defaultdict


class DataProcessor:
    def __init__(self, data, headers):
        self.data = data
        self.headers = headers
        self.operations = []

    def select(self, fields):
        for field in fields:
            if field not in self.headers:
                raise ValueError(f"Поле '{field}' не найдено.")
        self.operations.append(('select', fields))
        return self

    def sort(self, field, reverse=False):
        if field not in self.headers:
            raise ValueError(f"Поле для сортировки '{field}' не найдено.")
        self.operations.append(('sort', field, reverse))
        return self

    def group_by(self, field):
        if field not in self.headers:
            raise ValueError(f"Поле для группировки '{field}' не найдено.")
        self.operations.append(('group_by', field))
        return self

    def execute(self):
        result = self.data

        for op in sorted(self.operations, key=lambda x: {'group_by': 0, 'sort': 1, 'select': 2}[x[0]]):
            if op[0] == 'group_by':
                grouped = defaultdict(list)
                for row in result:
                    grouped[row[op[1]]].append(row)
                result = grouped
            elif op[0] == 'sort':
                if isinstance(result, dict):
                    for key in result:
                        result[key] = sorted(result[key], key=lambda x: x[op[1]], reverse=op[2])
                else:
                    result = sorted(result, key=lambda x: x[op[1]], reverse=op[2])
            elif op[0] == 'select':
                if isinstance(result, dict):
                    for key in result:
                        result[key] = [{k: row[k] for k in op[1]} for row in result[key]]
                else:
                    result = [{k: row[k] for k in op[1]} for row in result]

        return result
