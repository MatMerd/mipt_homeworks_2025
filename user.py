from entity.request import Request
from statistic import Statistic
from typing import Any


class User:
    def __init__(self, name: str):
        self.name = name
        self.requests = []

    def process_request(self, request: Request) -> list[dict[str, Any]]:
        self.requests.append(request)
        # sorting, grouping, choosing...
        repos = [[], [], []]
        stats = []
        for group in repos:
            stat = Statistic.get_all_statistics(group)
            stats.append(stat)

        return stats
