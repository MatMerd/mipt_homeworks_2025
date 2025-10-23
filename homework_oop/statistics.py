from typing import List, Dict, Any, Callable


class RepositoryStatistics:
    @staticmethod
    def _get_limit_rows(
        data: List[Dict[str, Any]], field: str, reverse: bool = False, limit: int = -1
    ) -> List[Dict[str, Any]]:
        if not data:
            return []

        sorted_data = sorted(data, key=lambda x: x[field], reverse=reverse)
        value = sorted_data[0][field]

        result = [row for row in sorted_data if row[field] == value]

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
    def min(
        data: List[Dict[str, Any]], field: str, limit: int = -1
    ) -> List[Dict[str, Any]]:
        return RepositoryStatistics._get_limit_rows(data, field, limit=limit)

    @staticmethod
    def max(
        data: List[Dict[str, Any]], field: str, limit: int = -1
    ) -> List[Dict[str, Any]]:
        return RepositoryStatistics._get_limit_rows(data, field, limit=limit)

    @staticmethod
    def median(data: List[Dict[str, Any]], field: str) -> List[Dict[str, Any]]:
        if not data:
            return []

        sorted_data = sorted(data, key=lambda x: x[field])
        n = len(sorted_data)

        if n % 2 == 1:
            median_value = sorted_data[n // 2][field]
        else:
            left = sorted_data[n // 2 - 1][field]
            right = sorted_data[n // 2][field]
            median_value = (left + right) / 2

        result = [row for row in sorted_data if row[field] == median_value]

        if not result and n > 1:
            result = [sorted_data[n // 2 - 1], sorted_data[n // 2]]

        return result

    @staticmethod
    def select_by_predicate(
        data: List[Dict[str, Any]], field: str, predicate: Callable, limit: int = -1
    ) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []

        for row in data:
            if predicate(row[field]):
                if limit != -1 and len(result) == limit:
                    break
                result.append(row)
        return result

    @staticmethod
    def selection_by_value(
        data: List[Dict[str, Any]],
        field: str,
        value: int | float,
        eps: int | float,
        limit: int = -1,
    ) -> List[Dict[str, Any]]:
        return RepositoryStatistics.select_by_predicate(
            data, field, lambda x: abs(x - value) <= eps, limit
        )
