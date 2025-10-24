from entity.group_type import GroupType
from entity.repository import Repository
from entity.request import Request
from entity.sort_type import SortType
from entity.where_type import WhereType


class Sorting:

    @staticmethod
    def __where(predicates: dict[WhereType, str], repositories: list[Repository]) -> list[Repository]:
        result = []
        for repository in repositories:
            flag = True
            for predicate in predicates:
                value = getattr(repository, predicate.name.lower())
                if value != predicates[predicate]:
                    flag = False
                    break
            if flag:
                result.append(repository)
        return result

    @staticmethod
    def __group(predicates: set[GroupType], repositories: list[Repository]) -> list[list[Repository]]:
        cnt = {}
        for repository in repositories:
            current_fields = {}
            for predicate in predicates:
                value = getattr(repository, predicate.name.lower())
                current_fields[predicate] = value
            key = Sorting.__dict_to_key(current_fields)
            if key not in cnt:
                cnt[key] = []
            cnt[key].append(repository)
        result = []
        for value in cnt.values():
            result.append(value)
        return result

    @staticmethod
    def __sort(predicates: list[SortType], bag_repositories: list[list[Repository]]) -> list[list[Repository]]:
        result = []
        for repositories in bag_repositories:
            sorted_repositories = sorted(repositories, key=lambda repo: Sorting.__get_sort_key(repo, predicates))
            result.append(sorted_repositories)
        return result

    @staticmethod
    def __get_sort_key(repository, predicates: list[SortType]):
        return tuple(getattr(repository, field.name.lower()) for field in predicates)

    @staticmethod
    def __dict_to_key(d: dict[GroupType, str]) -> tuple:
        return tuple(sorted(d.items()))

    @staticmethod
    def execute_request(request: Request, repositories: list[Repository]) -> list[list[Repository]]:
        repositories = Sorting.__where(request.where_by, repositories)
        repositories = Sorting.__group(request.group_by, repositories)
        repositories = Sorting.__sort(request.sort_by, repositories)
        return repositories
