from datetime import datetime
from functools import cmp_to_key
from typing import Any

from repository import Repository
from user import User
from writer import Writer
import constants


class Methods:
    def _compare_to(self, arg1, arg2, compare_operator: str) -> bool:
        if arg1 in [None, "None", "", "null", "<null>"] or arg2 in [
            None,
            "None",
            "",
            "null",
            "<null>",
        ]:
            return False
        if compare_operator == "==":
            return arg1 == arg2
        if compare_operator == "!=":
            return arg1 != arg2
        if compare_operator == "<":
            return arg1 < arg2
        if compare_operator == ">":
            return arg1 > arg2
        if compare_operator == "<=":
            return arg1 <= arg2
        return arg1 >= arg2

    def _get_repository_field_by_name(
        self, repository: Repository, field_name: str
    ) -> Any:
        return repository.__getattribute__(field_name)

    def _universal_compare_to(
        self,
        repo1: Repository,
        repo2: Repository,
        field: str,
        order: str,
        modifier: str,
    ) -> int:
        repo1_field: Any = self._get_repository_field_by_name(repo1, field)
        repo2_field: Any = self._get_repository_field_by_name(repo2, field)
        if order == "increase":
            if modifier == "" or modifier == "alphabet":
                if self._compare_to(repo1_field, repo2_field, "<="):
                    return -1
                return 1
            elif modifier == "length" or modifier == "size":
                if self._compare_to(len(repo1_field), len(repo2_field), "<="):
                    return -1
                return 1
        else:
            if modifier == "" or modifier == "alphabet":
                if self._compare_to(repo1_field, repo2_field, ">="):
                    return -1
                return 1
            elif modifier == "length" or modifier == "size":
                if self._compare_to(len(repo1_field), len(repo2_field), ">="):
                    return -1
                return 1
        return 0

    def _create_comparator_with_params(
        self, field: str, order: str, modifier: str
    ) -> Any:
        return cmp_to_key(
            lambda repo1, repo2: self._universal_compare_to(
                repo1, repo2, field, order, modifier
            )
        )

    def _get_result_of_one_filter_query(
        self, repository: Repository, query_array: list[str]
    ) -> bool:
        field: Any = self._get_repository_field_by_name(repository, query_array[1])
        if query_array[1] in constants.int_fields:
            return self._compare_to(field, int(query_array[3]), query_array[2])
        if query_array[1] in constants.bool_fields:
            condition: bool = True if query_array[2] == "true" else False
            return self._compare_to(field, condition, "==")
        if query_array[1] in constants.datetime_fields:
            condition_dt: datetime = datetime.fromisoformat(
                query_array[3].replace("Z", "+00:00")
            )
            return self._compare_to(field, condition_dt, query_array[2])
        if query_array[1] in constants.array_fields:
            return query_array[3] in field
        if query_array[2] == "alphabet":
            return self._compare_to(field, query_array[4], query_array[3])
        if query_array[2] == "length":
            return self._compare_to(len(field), int(query_array[4]), query_array[3])
        return query_array[3] in field

    def filter(
        self, repositories: list[Repository], filter_queries: list[str]
    ) -> list[Repository]:
        ans: list[Repository] = []
        for repository in repositories:
            result: bool = True
            for query in filter_queries:
                if not self._get_result_of_one_filter_query(
                    repository, query.split(" ")
                ):
                    result = False
                    break
            if result:
                ans.append(repository)
        return ans

    def sort(
        self, repositories: list[Repository], sort_queries: list[str]
    ) -> list[Repository]:
        for sort_query in sort_queries[::-1]:
            query_array: list[str] = sort_query.strip().split(" ")
            field: str = query_array[2]
            order: str = query_array[1]
            modifier: str = "" if len(query_array) == 3 else query_array[3]
            repositories = sorted(
                repositories,
                key=self._create_comparator_with_params(field, order, modifier),
            )
        return repositories

    def group_by(self, repositories: list[Repository], query: str) -> list[Repository]:
        query_array: list[str] = query.strip().split(" ")
        field: str = query_array[1]
        if field in constants.str_fields:
            repositories = self.sort(
                repositories, ["sort increase " + field + " alphabet"]
            )
        elif field in constants.array_fields:
            repositories = self.sort(repositories, ["sort increase " + field + " size"])
        else:
            repositories = self.sort(repositories, ["sort increase " + field])
        return repositories

    def help(self, query_array: list[str]) -> None:
        file = open("helper/" + query_array[1] + ".txt", "r", encoding="utf-8")
        string: str = file.read()
        file.close()
        print(string)

    def execute(
        self, user: User, writer: Writer, repositories: list[Repository], query: str
    ) -> list[Repository]:
        query_array: list[str] = query.strip().split(" ")
        if query_array[0] == "save":
            repositories = self.filter(repositories, user.get_special_queries("filter"))
            repositories = self.sort(repositories, user.get_special_queries("sort"))
            if len(user.get_special_queries("group_by")) > 0:
                repositories = self.group_by(
                    repositories, user.get_special_queries("group_by")[0]
                )
            writer.write(repositories, query_array[1], query_array[2])
        elif query_array[0] == "help":
            self.help(query_array)
        return repositories
