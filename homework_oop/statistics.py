from typing import List, Callable

from homework_oop.repository.repomodel import Repository


class RepositoryStatistics:
    @staticmethod
    def _get_limit_rows(
        data: List[Repository], field: str, reverse: bool = False, limit: int = -1
    ) -> List[Repository]:
        if not data:
            return []

        sorted_data = sorted(data, key=lambda x: x.get_field(field), reverse=reverse)
        value = sorted_data[0].get_field(field)

        result = [row for row in sorted_data if row.get_field(field) == value]

        if limit == -1:
            return result

        if limit <= len(result):
            return result[:limit]

        i = len(result)
        while i < len(sorted_data) and len(result) < limit:
            result.append(sorted_data[i])
            i += 1

        return result

    @staticmethod
    def min(data: List[Repository], field: str, limit: int = -1) -> List[Repository]:
        return RepositoryStatistics._get_limit_rows(data, field, limit=limit)

    @staticmethod
    def max(data: List[Repository], field: str, limit: int = -1) -> List[Repository]:
        return RepositoryStatistics._get_limit_rows(data, field, limit=limit)

    @staticmethod
    def median(data: List[Repository], field: str) -> List[Repository]:
        if not data:
            return []

        sorted_data = sorted(data, key=lambda x: x.get_field(field))
        n = len(sorted_data)

        if n % 2 == 1:
            median_value = sorted_data[n // 2].get_field(field)
        else:
            left = sorted_data[n // 2 - 1].get_field(field)
            right = sorted_data[n // 2].get_field(field)
            median_value = (left + right) / 2

        result = [row for row in sorted_data if row.get_field(field) == median_value]

        if not result and n > 1:
            result = [sorted_data[n // 2 - 1], sorted_data[n // 2]]

        return result

    @staticmethod
    def select_by_predicate(
        data: List[Repository], field: str, predicate: Callable, limit: int = -1
    ) -> List[Repository]:
        result: List[Repository] = []

        for row in data:
            if predicate(row.get_field(field)):
                if limit != -1 and len(result) == limit:
                    break
                result.append(row)
        return result

    @staticmethod
    def selection_by_value(
        data: List[Repository],
        field: str,
        value: int | float,
        eps: int | float,
        limit: int = -1,
    ) -> List[Repository]:
        return RepositoryStatistics.select_by_predicate(
            data, field, lambda x: abs(x - value) <= eps, limit
        )
