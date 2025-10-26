from datetime import datetime

import constants
from syntax_error import SyntaxError
from user import User


class SyntaxChecker:
    def __init__(self) -> None:
        self._syntax_error: SyntaxError = SyntaxError()
        self.was_group_by: bool = False
        self.last_query: str = ""

    def _is_int(self, string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

    def _is_bool(self, string: str) -> bool:
        return string == "true" or string == "false"

    def _is_datetime(self, string: str):
        try:
            if string.endswith("Z"):
                string = string[:-1] + "+00:00"
            datetime.fromisoformat(string)
            return True
        except ValueError:
            return False

    def check(self, query: str, user: User) -> bool:
        query_array: list[str] = query.strip().split(" ")
        command: str = query_array[0]
        if command == "filter":
            return self._check_filter(query_array)
        elif command == "save":
            return self._check_save(query_array)
        elif command == "stop":
            return len(query_array) == 1
        elif command == "help":
            return self._check_help(query_array)
        elif command == "reset":
            return len(query_array) == 1
        elif command == "sort":
            return self._check_sort(query_array)
        elif command == "group_by":
            return self._check_group_by(query_array)
        elif command == "save_query":
            return self._check_save_query(query_array, user)
        elif command == "call":
            return self._check_call(query_array, user)
        elif command == "get_statistics":
            return self._check_get_statistics(query_array)
        self._syntax_error.raise_command_not_found_exception()
        return False

    def check_command_need_to_execute(self, query) -> bool:
        query_array: list[str] = query.strip().split(" ")
        command: str = query_array[0]
        if command in ["filter", "sort", "group_by"]:
            return False
        return True

    def _check_filter(self, query_array: list[str]) -> bool:
        if len(query_array) < 2:
            self._syntax_error.raise_empty_field_exception("filter")
            return False
        field: str = query_array[1]
        if field in constants.int_fields:
            return self._check_filter_for_int(query_array)
        elif field in constants.str_fields:
            return self._check_filter_for_str(query_array)
        elif field in constants.bool_fields:
            return self._check_filter_for_bool(query_array)
        elif field in constants.datetime_fields:
            return self._check_filter_for_datetime(query_array)
        elif field in constants.array_fields:
            return self._check_filter_for_array(query_array)
        self._syntax_error.raise_empty_field_exception("filter")
        return False

    def _check_filter_for_int(self, query_array: list[str]) -> bool:
        if len(query_array) == 4:
            if query_array[2] in constants.compare_operators and self._is_int(
                query_array[3]
            ):
                return True
        self._syntax_error.raise_uncorrect_condition_exception("filter")
        return False

    def _check_filter_for_str(self, query_array: list[str]) -> bool:
        if len(query_array) == 4:
            if query_array[2] == "contains":
                return True
        elif len(query_array) == 5:
            if query_array[2] == "alphabet":
                if query_array[3] in constants.compare_operators:
                    return True
            elif query_array[2] == "length":
                if query_array[3] in constants.compare_operators and self._is_int(
                    query_array[4]
                ):
                    return True
        self._syntax_error.raise_uncorrect_condition_exception("filter")
        return False

    def _check_filter_for_bool(self, query_array: list[str]) -> bool:
        if len(query_array) == 3:
            if self._is_bool(query_array[2]):
                return True
        self._syntax_error.raise_uncorrect_condition_exception("filter")
        return False

    def _check_filter_for_datetime(self, query_array: list[str]) -> bool:
        if len(query_array) == 4:
            if query_array[2] in constants.compare_operators and self._is_datetime(
                query_array[3]
            ):
                return True
        self._syntax_error.raise_uncorrect_condition_exception("filter")
        return False

    def _check_filter_for_array(self, query_array: list[str]) -> bool:
        if len(query_array) == 4 and query_array[2] == "contains":
            return True
        self._syntax_error.raise_uncorrect_condition_exception("filter")
        return False

    def _check_save(self, query_array: list[str]) -> bool:
        if len(query_array) == 3 and query_array[1] in ["txt", "csv", "json"]:
            return True
        self._syntax_error.raise_uncorrect_condition_exception("save")
        return False

    def _check_help(self, query_array: list[str]) -> bool:
        if len(query_array) == 2:
            if query_array[1] in constants.commands or query_array[1] in [
                "full_syntax",
                "commands",
                "fields",
                "compare_operators",
            ]:
                return True
        self._syntax_error.raise_uncorrect_condition_exception("help")
        return False

    def _check_sort(self, query_array: list[str]) -> bool:
        if query_array[1] in ["increase", "decrease"]:
            if len(query_array) == 3:
                if query_array[2] in constants.int_fields:
                    return True
                elif query_array[2] in constants.bool_fields:
                    return True
                elif query_array[2] in constants.datetime_fields:
                    return True
            elif len(query_array) == 4:
                if query_array[2] in constants.str_fields:
                    if query_array[3] in ["alphabet", "length"]:
                        return True
                elif query_array[2] in constants.array_fields:
                    if query_array[3] == "size":
                        return True
        self._syntax_error.raise_uncorrect_condition_exception("sort")
        return False

    def _check_group_by(self, query_array: list[str]) -> bool:
        if query_array[1] in constants.all_fields:
            if not self.was_group_by:
                self.was_group_by = True
                return True
            self._syntax_error.raise_more_than_one_group_by_exception()
            return False
        self._syntax_error.raise_uncorrect_condition_exception("group_by")
        return False

    def _check_save_query(self, query_array: list[str], user: User) -> bool:
        if len(query_array) == 2:
            if len(user.get_queries()) > 0:
                return True
            self._syntax_error.raise_cannot_use_save_query()
            return False
        self._syntax_error.raise_uncorrect_condition_exception("save_query")
        return False

    def _check_call(self, query_array: list[str], user: User) -> bool:
        if len(query_array) == 2:
            if user.has_query_by_name(query_array[1]):
                return True
            self._syntax_error.raise_query_not_found_exception()
            return False
        self._syntax_error.raise_uncorrect_condition_exception("call")
        return False

    def _check_get_statistics(self, query_array: list[str]) -> bool:
        if len(query_array) == 5:
            if (
                query_array[1] == "cnt"
                and query_array[2] == "in"
                and query_array[3] in ["txt", "csv", "json"]
            ):
                return True
        elif len(query_array) == 6:
            if (
                query_array[1] in ["median", "avg"]
                and query_array[2] in constants.int_fields
                and query_array[3] == "in"
                and query_array[4] in ["txt", "csv", "json"]
            ):
                return True
        elif len(query_array) == 8:
            if (
                query_array[1] == "top"
                and query_array[3] in ["min", "max"]
                and self._is_int(query_array[2])
            ):
                if (
                    int(query_array[2]) > 0
                    and query_array[4] in constants.int_fields
                    and query_array[5] == "in"
                    and query_array[6] in ["txt", "csv", "json"]
                ):
                    return True
        self._syntax_error.raise_uncorrect_condition_exception("get_statistics")
        return False

    def raise_more_than_one_group_by_exception(self) -> None:
        return self._syntax_error.raise_more_than_one_group_by_exception()
