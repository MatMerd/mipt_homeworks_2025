import difflib


class Query:
    def __init__(self, data):
        self.data = data
        self.queries = []

    def sort(self, *args):
        self.queries.append({'sort': args})
        return self

    def group(self, *args):
        self.queries.append({'group': args})
        return self

    def select(self, *args):
        self.queries.append({'select': args})
        return self

    def execute(self):
        for query in self.queries:
            for key, value in query.items():
                if key == 'sort':
                    self.sorting(value)
                elif key == 'group':
                    self.data = self.grouping(value)
                elif key == 'select':
                    self.data = self.selecting(value)
        return self.data

    def check_columns_exist(self, columns):
        if not self.data:
            raise ValueError("Невозможно выполнить операцию: data пустой.")

        valid_columns = self.data[0].keys()
        for col in columns:
            if col not in valid_columns:
                suggestion = difflib.get_close_matches(col, valid_columns, n=1)
                msg = f"Колонка '{col}' не найдена."
                if suggestion:
                    msg += f" Возможно, вы имели в виду '{suggestion[0]}'"
                raise ValueError(msg)

    def sorting(self, columns):
        self.check_columns_exist(columns)
        for col in reversed(columns):
            if all(str(x[col]).isdigit() for x in self.data):
                self.data = sorted(self.data, key=lambda x: int(x[col]))
            else:
                self.data = sorted(self.data, key=lambda x: x[col])

    def grouping(self, columns):
        self.check_columns_exist(columns)
        grouped = {}
        for row in self.data:
            key = tuple(row[column] for column in columns)
            grouped.setdefault(key, []).append(row)
        return grouped

    def selecting(self, columns):
        self.check_columns_exist(columns)
        result = []
        for row in self.data:
            new_row = {col: row[col] for col in columns if col in row}
            result.append(new_row)
        return result
