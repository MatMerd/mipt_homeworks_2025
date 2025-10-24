from homework_oop.QueryProcessor import QueryProcessor


class User:
    def __init__(self, name):
        self.name = name
        self.saved_queries = {}

    def save_query(self, query_name, query_processor):
        self.saved_queries[query_name] = {"operations" : query_processor.operations}

    def run_query(self, query_name, data):
        if query_name not in self.saved_queries:
            raise ValueError(f"Запрос '{query_name}' не найден")

        query_processor = QueryProcessor(data)
        query_processor.operations = self.saved_queries[query_name]["operations"]
        return query_processor.execute()
