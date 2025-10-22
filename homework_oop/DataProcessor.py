import typing
from dataclasses import dataclass, field
import functools

CsvRow: typing.TypeAlias = dict[str, object]
CsvTable: typing.TypeAlias = list[CsvRow]

ProcessingResult: typing.TypeAlias = CsvTable | dict[object, CsvTable]


@dataclass
class DataProcessor:
    _filters: list[tuple[str, object]] = field(default_factory=list)
    _sort_by: list[tuple[str, bool]] = field(default_factory=list)
    _group_by: list[str] = field(default_factory=list)

    def copy(self) -> typing.Self:
        result = DataProcessor()
        result._filters = self._filters.copy()
        result._sort_by = self._sort_by.copy()
        result._group_by = self._group_by.copy()
        return result

    @staticmethod
    def _get_field(row: CsvRow, field_name: str) -> object:
        if field_name in row:
            return row[field_name]
        else:
            raise KeyError(f'Table does not contain field \'{field_name}\'')

    def filter(self, field_name: str, value: object) -> typing.Self:
        self._filters.append((field_name, value))
        return self

    def _matches_filters(self, row: CsvRow) -> bool:
        return all(self._get_field(row, field_name) == value for field_name, value in self._filters)

    def sort(self, by_field: str, reverse: bool = False) -> typing.Self:
        self._sort_by.append((by_field, reverse))
        return self

    def _sort_data(self, data: CsvTable) -> CsvTable:
        result = data.copy()
        for key, reverse in reversed(self._sort_by):
            result.sort(key=functools.partial(self._get_field, key), reverse=reverse)
        return result

    def group(self, by_field: str) -> typing.Self:
        self._group_by.append(by_field)
        return self

    def _group_key(self, row: CsvRow) -> object:
        if len(self._group_by) > 1:
            return tuple(self._get_field(row, key) for key in self._group_by)
        else:
            return self._get_field(row, self._group_by[0])

    def _group_data(self, data: CsvTable) -> dict[object, CsvTable]:
        result = {}
        for item in data:
            key = self._group_key(item)
            result.setdefault(key, [])
            result[key].append(item)
        return result

    def process(self, data: list[dict[str, object]]) -> ProcessingResult:
        filtered_data = [item for item in data if self._matches_filters(item)]
        sorted_data = self._sort_data(filtered_data)

        if self._group_by:
            return self._group_data(sorted_data)
        else:
            return sorted_data
