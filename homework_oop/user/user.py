from homework_oop.data_processor.data_processor import DataProcessor


class User:
    __slots__ = ("__name", "__saved_queries")

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__saved_queries = {}

    def save_query(self, query_name: str, query_processor: DataProcessor):
        self.__saved_queries[query_name] = query_processor
        print(f"Пользователь '{self.__name}' сохранил запрос '{query_name}'.")

    def execute_saved_query(self, query_name: str):
        if query_name in self.__saved_queries:
            print(f"Выполнение сохраненного запроса '{query_name}'...")
            query_processor = self.__saved_queries[query_name]
            return query_processor.execute()
        else:
            raise ValueError(f"Запрос с именем '{query_name}' не найден.")

    def get_all_query_names(self) -> list[str]:
        return list(self.__saved_queries.keys())
