from entity.group_type import GroupType
from entity.repository import Repository
from entity.request import Request
from entity.sort_type import SortType
from entity.where_type import WhereType
from sorting import Sorting
from statistic import Statistic
from typing import Any


class User:
    def __init__(self, name: str):
        self.name = name
        self.__requests = []

    def process_request(self, request: Request, repositories: list[Repository]) -> list[dict[str, Any]]:
        self.__requests.append(request)
        repos = Sorting.execute_request(request, repositories)
        stats = []
        for group in repos:
            stat = Statistic.get_all_statistics(group)
            stats.append(stat)

        return stats

    def get_request_history(self) -> list[Request]:
        return self.__requests

    def get_request(self, index: int) -> Request:
        return self.__requests[index]

    @staticmethod
    def create_request(sort_by: list[SortType], group_by: set[GroupType],
                       where_by: dict[WhereType, str]) -> Request:
        return Request(sort_by, group_by, where_by)
