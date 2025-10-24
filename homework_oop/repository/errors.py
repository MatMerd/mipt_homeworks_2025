from typing import Optional, Dict, Any


class FilterError(Exception):
    def __init__(
        self, query: Dict[str, Any], original_error: Optional[Exception] = None
    ):
        super().__init__(f"Filter error for query {query}")
        self.__cause__ = original_error


class SortingError(Exception):
    def __init__(
        self, field: Optional[str], original_error: Optional[Exception] = None
    ):
        self.field = field
        super().__init__(f"Sorting error for field '{field}'")
        self.__cause__ = original_error


class GroupingError(Exception):
    def __init__(
        self, field: Optional[str], original_error: Optional[Exception] = None
    ):
        self.field = field
        super().__init__(f"Grouping error for field '{field}'")
        self.__cause__ = original_error
