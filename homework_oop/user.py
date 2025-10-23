import typing as tp
import data_handler

class User:
    """
    Класс пользователя, который может сохранять и выполнять свои "запросы" 
    (цепочки операций DataHandler)
    """
    def __init__(self, name: str):
        self.name = name
        self.saved_queries: tp.Dict[str, tp.List[tp.Tuple[str, tp.Any]]] = {}

    def save_query(self, query_name: str, operations: tp.List[tp.Tuple[str, tp.Any]]) -> None:
        """
        Сохранение цепочки операций DataHandler под именем query_name для текущего пользователя
        :param query_name: имя запроса
        :param operations: список операций в формате [(операция, параметр)]
        """
        self.saved_queries.update({query_name : operations})
        print(f"Запрос '{query_name}' сохранён для пользователя {self.name}.")

    def run_query(self, query_name: str, handler: data_handler.DataHandler) -> tp.Any:
        """
        Выполнение сохранённого запроса с помощью переданного DataHandler
        :param query_name: имя сохранённого запроса
        :param handler: экземпляр DataHandler, над которым будет выполнен запрос
        :return: результат выполнения запроса
        :raises ValueError: если запрос с таким именем не был сохранён
        """
        if query_name not in self.saved_queries.keys():
            raise ValueError(f"Запрос {query_name} не был сохранен!")
        
        handler.operations = self.saved_queries[query_name]
        return handler.execute()
