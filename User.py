import Query

class User:
    def __init__(self, data):
        self.data = data
        self.saved_queries = []

    def save_query(self, operation, *columns):
        if operation not in ("select", "group", "sort"):
            raise ValueError(f"Недопустимая операция '{operation}'. Возможные: select, group, sort")

        query_info = {
            "operation": operation,
            "columns": columns
        }

        self.saved_queries.append(query_info)

    def run_queries(self):
        query = Query.Query(self.data)

        for query_info in self.saved_queries:
            operation = query_info["operation"]
            columns = query_info["columns"]

            if operation == "select":
                query.select(*columns)
            elif operation == "group":
                query.group(*columns)
            elif operation == "sort":
                query.sort(*columns)

        result = query.execute()
        self.data = result
