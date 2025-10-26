from methods import Methods
from repository import Repository
from writer import Writer


class StatisticsCounter:
    def __init__(self, methods: Methods, writer: Writer) -> None:
        self._methods = methods
        self._writer = writer

    def count_statistics(self, repositories: list[Repository], query: str) -> None:
        query_array: list[str] = query.strip().split(" ")
        field_name: str = ""
        file_format: str = ""
        file_name: str = ""
        if query_array[1] == "cnt":
            file_format = query_array[3]
            file_name = query_array[4]
            self._writer.write_number("cnt", len(repositories), file_format, file_name)
        elif query_array[1] == "median":
            field_name = query_array[2]
            file_format = query_array[4]
            file_name = query_array[5]
            sorted_repositories = self._methods.sort(
                repositories, ["sort increase " + field_name]
            )
            median: float = 0
            if len(sorted_repositories) > 0:
                size: int = len(sorted_repositories)
                if size % 2 == 0:
                    value1: int = repositories[size // 2].__getattribute__(field_name)
                    value2: int = repositories[(size - 1) // 2].__getattribute__(
                        field_name
                    )
                    median = (value1 + value2) / 2
                else:
                    median = repositories[size // 2].__getattribute__(field_name)
            self._writer.write_number("median", median, file_format, file_name)
        elif query_array[1] == "avg":
            field_name = query_array[2]
            file_format = query_array[4]
            file_name = query_array[5]
            summ: int = 0
            for repository in repositories:
                summ += repository.__getattribute__(field_name)
            if len(repositories) > 0:
                avg: float = summ / len(repositories)
                self._writer.write_number("avg", avg, file_format, file_name)
            else:
                self._writer.write_number("avg", 0.0, file_format, file_name)
        else:
            top: int = int(query_array[2])
            min_or_max: str = query_array[3]
            field_name = query_array[4]
            file_format = query_array[6]
            file_name = query_array[7]
            order: str = "increase" if min_or_max == "min" else "decrease"
            sorted_repositories = self._methods.sort(
                repositories, ["sort " + order + " " + field_name]
            )
            right_index: int = min(len(sorted_repositories), top)
            self._writer.write(
                sorted_repositories[:right_index:], file_format, file_name
            )
