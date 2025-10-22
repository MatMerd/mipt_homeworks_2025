import typing


class DataProcessor:
    _filters: list[tuple[str, object]]
    _sort_by: list[tuple[str, bool]]
    _group_by: list[str]

    def __init__(self):
        self._filters = []
        self._sort_by = []
        self._group_by = []

    def filter(self, field: str, value: object) -> typing.Self:
        self._filters.append((field, value))
        return self

    def _matches_filters(self, item: dict[str, object]) -> bool:
        return all(item[field] == value for field, value in self._filters)

    def sort(self, by_field: str, reverse: bool = False) -> typing.Self:
        self._sort_by.append((by_field, reverse))
        return self

    def _sort_data(self, data: list[dict[str, object]]) -> list[dict[str, object]]:
        result = data.copy()
        for key, reverse in reversed(self._sort_by):
            result.sort(key=lambda item: item[key], reverse=reverse)
        return result

    def group(self, by_field: str) -> typing.Self:
        self._group_by.append(by_field)
        return self

    def _group_key(self, item: dict[str, object]) -> object | tuple[object]:
        if len(self._group_by) > 1:
            return tuple(item[key] for key in self._group_by)
        else:
            return item[self._group_by[0]]

    def _group_data(self, data: list[dict[str, object]]) -> dict[object, list[dict[str, object]]] | dict[
            tuple, list[dict[str, object]]]:
        result = {}
        for item in data:
            key = self._group_key(item)
            result.setdefault(key, [])
            result[key].append(item)
        return result

    def process(self, data: list[dict[str, object]]) -> list[dict[str, object]] | dict[
            object, list[dict[str, object]]] | dict[tuple, list[dict[str, object]]]:
        filtered_data = [item for item in data if self._matches_filters(item)]
        sorted_data = self._sort_data(filtered_data)

        if self._group_by:
            return self._group_data(sorted_data)
        else:
            return sorted_data
