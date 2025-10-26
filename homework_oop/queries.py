from typing import Any, Callable, Dict, List, Tuple, Optional, cast
from difflib import get_close_matches
from collections import defaultdict
from copy import deepcopy
from homework_oop.repository import Repository

# вот если честно сейчас хз как органировать запросы и как их обрабатывать. вроде и логично, что сначала select, потом group
# потом sort. но я хз как нормально организовать group, поэтому тут сначала select, потом sort, потом group.


class Projection:
    availible_fields: List[str] = [
        Repository.attr_to_csv_key(field)
        for field in Repository.__dataclass_fields__.keys()
    ]

    def __init__(self, data: List[Repository]):
        self._source: List[Repository] = data
        self._sort_keys: List[Tuple[str, bool]] = []
        self._group_keys: List[str] = []
        self._select_keys: List[str] = []
        self._filters: List[Callable[[Repository], bool]] = []

        self._result: Optional[
            List[Dict[str, Any]] | Dict[Tuple[Any, ...], List[Dict[str, Any]]]
        ] = None

    def sort_by(self, *keys: str, reverse: bool = False) -> "Projection":
        for key in keys:
            key = self._ensure_field(key)
            self._sort_keys.append((key, reverse))

        return self

    def group_by(self, *keys: str) -> "Projection":
        for key in keys:
            key = self._ensure_field(key)
            self._group_keys.append(key)

        return self

    def select(self, *keys: str) -> "Projection":
        for key in keys:
            key = self._ensure_field(key)
            self._select_keys.append(key)

        return self

    def filter(self, *conditions: Callable[[Repository], bool]) -> "Projection":
        for condition in conditions:
            self._filters.append(condition)

        return self

    def execute(
        self,
    ) -> List[Dict[str, Any]] | Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
        repos: List[Repository] = self._apply_filters(self._source)

        rows: List[Dict[str, Any]] = self._select_data(repos)

        if self._sort_keys:
            rows = self._sort_data(rows)

        if self._group_keys:
            grouped = self._group_data(rows)
            self._result = grouped
            return grouped

        self._result = rows
        return rows

    @property
    def select_keys(self) -> List[str]:
        return self._select_keys

    @property
    def sort_keys(self) -> List[Tuple[str, bool]]:
        return self._sort_keys

    @property
    def group_keys(self) -> List[str]:
        return self._group_keys

    @property
    def filters(self) -> List[Callable[[Repository], bool]]:
        return self._filters

    @property
    def result(
        self,
    ) -> Optional[List[Dict[str, Any]] | Dict[Tuple[Any, ...], List[Dict[str, Any]]]]:
        return self._result

    def _apply_filters(self, data: List[Repository]) -> List[Repository]:
        filtered_data = data

        for condition in self._filters:
            filtered_data = [repo for repo in filtered_data if condition(repo)]

        return filtered_data

    def _select_data(self, data: List[Repository]) -> List[Dict[str, Any]]:
        selected_fields: List[str] = self._select_keys or list(self.availible_fields)

        result: List[Dict[str, Any]] = []

        for repo in data:
            row: Dict[str, Any] = {}
            for csv_key in selected_fields:
                attr = Repository.csv_key_to_attr(csv_key)
                row[csv_key] = deepcopy(getattr(repo, attr))
            result.append(row)

        return result

    def _sort_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        selected_fields = set(self._select_keys or self.availible_fields)

        for key, _ in self._sort_keys:
            if key not in selected_fields:
                raise ValueError(f"Sort key '{key}' must be part of the selection")

        for key, reverse in reversed(self._sort_keys):
            data.sort(key=lambda r: cast(Any, r.get(key)), reverse=reverse)

        return data

    def _group_data(
        self, data: List[Dict[str, Any]]
    ) -> Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
        selected_fields = set(self._select_keys or self.availible_fields)
        for gk in self._group_keys:
            if gk not in selected_fields:
                raise ValueError(f"Group key '{gk}' must be part of the selection")

        grouped: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
        for row in data:
            group_key: Tuple[Any, ...] = tuple(row.get(k) for k in self._group_keys)
            grouped[group_key].append(row)

        return dict(grouped)

    def _ensure_field(self, key: str) -> str:
        attr = Repository.csv_key_to_attr(key)

        if hasattr(Repository, attr):
            return key

        close_matches = get_close_matches(key, self.availible_fields, n=1)
        if close_matches:
            raise ValueError(
                f"Invalid field '{key}'. Did you mean '{close_matches[0]}'?"
            )
        raise ValueError(f"Invalid field '{key}'")
