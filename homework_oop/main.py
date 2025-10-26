from typing import Any

from csv_reader import CSVReader
from methods import Methods
from repository import Repository
from statistics_counter import StatisticsCounter
from syntax_checker import SyntaxChecker
from user import User
from writer import Writer


def get_repository_list(file: Any) -> list[Repository]:
    repositories: list[Repository] = []
    for list_repository in file:
        repository: Repository = Repository(list_repository)
        repositories.append(repository)
        """
        try:
            repository: Repository = Repository(list_repository)
            repositories.append(repository)
        except Exception:
            pass
        """
    return repositories


print("Файл загружается, пожалуйста, подождите...")
csv_reader: CSVReader = CSVReader()
file: list[list[str]] = csv_reader.read("repositories.csv")
repositories: list[Repository] = get_repository_list(file)
print("Файл загружен. Можете вводить команды.")
print('Если вы не знаете синтаксис, то введите "help help"')
user: User = User()
syntax_checker: SyntaxChecker = SyntaxChecker()
methods: Methods = Methods()
writer: Writer = Writer()
statistics_counter: StatisticsCounter = StatisticsCounter(methods, writer)
while True:
    query: str = input()
    if syntax_checker.check(query, user):
        if syntax_checker.check_command_need_to_execute(query):
            query_array: list[str] = query.strip().split(" ")
            if query_array[0] == "stop":
                print("Программа остановлена")
                break
            elif query_array[0] == "reset":
                repositories = get_repository_list(file)
                user.clear_queries()
                syntax_checker.was_group_by = False
                print("Изменения успешно отменены")
            elif query_array[0] == "save_query":
                user.save_query(query_array[1])
                user.clear_queries()
                syntax_checker.was_group_by = False
            elif query_array[0] == "call":
                queries: list[str] = user.get_query_by_name(query_array[1])
                for i in range(len(queries)):
                    current_query: str = queries[i]
                    if not syntax_checker.check(current_query, user):
                        break
                else:
                    user.add_queries(queries)
            elif query_array[0] == "get_statistics":
                statistics_counter.count_statistics(repositories, query)
            else:
                repositories = methods.execute(user, writer, repositories, query)
        else:
            user.add_query(query)
        syntax_checker.last_query = query
