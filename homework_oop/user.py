class User:
    def __init__(self) -> None:
        self._current_queries: list[str] = []
        self._saved_queries: dict[str, list[str]] = dict()

    def add_query(self, query: str) -> None:
        self._current_queries.append(query)

    def add_queries(self, queries: list[str]) -> None:
        self._current_queries += queries

    def clear_queries(self) -> None:
        self._current_queries = []

    def get_queries(self) -> list[str]:
        return self._current_queries

    def get_special_queries(self, query_type: str) -> list[str]:
        special_queries: list[str] = []
        for query in self._current_queries:
            query_array: list[str] = query.strip().split(" ")
            if query_type == "filter" and query_array[0] == "filter":
                special_queries.append(query)
            elif query_type == "sort" and query_array[0] == "sort":
                special_queries.append(query)
            elif query_type == "group_by" and query_array[0] == "group_by":
                special_queries.append(query)
        return special_queries

    def save_query(self, name: str) -> None:
        queries = self._current_queries.copy()
        self._saved_queries[name] = queries

    def has_query_by_name(self, name: str) -> bool:
        return True if name in self._saved_queries.keys() else False

    def get_query_by_name(self, name: str) -> list[str]:
        return self._saved_queries[name]
