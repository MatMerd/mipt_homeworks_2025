from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple, Any, Optional
from homework_oop.queries import Projection
from homework_oop.repository import Repository

# мы хотим репозиторий юзеров? чтоб не повторялись

# по тз написано что мы хотим "вызывать запросы", но как бы каждый раз его заново запускать так себе идея imo.
# добавила хранение самого реультата здесь в сохраненом запросе и в projection чтобы это осуществить


@dataclass
class SavedQuery:
    name: str
    select_keys: List[str] = None
    sort_keys: List[Tuple[str, bool]] = None
    group_keys: List[str] = None
    filters: List[Callable[[Repository], bool]] = None
    result: Optional[
        List[Dict[str, Any]] | Dict[Tuple[Any, ...], List[Dict[str, Any]]]
    ] = None


class User:
    def __init__(self, name: str):
        self.name = name
        self.saved_queries: Dict[str, SavedQuery] = {}

    def create_query(
        self,
        query_name: str,
        *,
        select: Optional[List[str]] = None,
        sort_by: Optional[List[Tuple[str, bool]]] = None,
        group_by: Optional[List[str]] = None,
        filters: Optional[List[Callable[[Repository], bool]]] = None,
    ) -> "User":
        if query_name in self.saved_queries:
            raise ValueError(f"Query with name {query_name} already exists")

        self.saved_queries[query_name] = SavedQuery(
            name=query_name,
            select_keys=select or [],
            sort_keys=sort_by or [],
            group_keys=group_by or [],
            filters=filters or [],
        )

        return self

    def save_existing_projection(
        self, query_name: str, projection: Projection
    ) -> "User":
        self.__check_query_existance(query_name)

        self.saved_queries[query_name] = SavedQuery(
            name=query_name,
            select_keys=projection.select_keys,
            sort_keys=projection.sort_keys,
            group_keys=projection.group_keys,
            filters=projection.filters,
            result=projection.result,
        )

        return self

    def execute_saved_query(
        self, query_name: str, data: List[Repository]
    ) -> List[Dict[str, Any]] | Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
        self.__check_query_existance(query_name)

        query = self.saved_queries[query_name]

        if query.result:
            return query.result

        projection = Projection(data)

        if query.filters:
            projection.filter(*query.filters)
        if query.select_keys:
            projection.select(*query.select_keys)
        if query.sort_keys:
            for key, reverse in query.sort_keys:
                projection.sort_by(key, reverse=reverse)
        if query.group_keys:
            projection.group_by(*query.group_keys)

        query.result = projection.execute()

        return query.result

    def update_saved_query(
        self,
        query_name: str,
        *,
        select: Optional[List[str]] = None,
        sort_by: Optional[List[Tuple[str, bool]]] = None,
        group_by: Optional[List[str]] = None,
        filters: Optional[List[Callable[[Repository], bool]]] = None,
    ) -> "User":
        self.__check_query_existance(query_name)

        query = self.saved_queries[query_name]

        if filters:
            query.filters = filters
        if select:
            query.select_keys = select
        if sort_by:
            query.sort_keys = sort_by
        if group_by:
            query.group_keys = group_by

        if query.result:
            query.result = None

        return self

    def delete_saved_query(self, query_name: str) -> "User":
        self.__check_query_existance(query_name)

        del self.saved_queries[query_name]

        return self

    def list_saved_queries(self) -> List[str]:
        return list(self.saved_queries.keys())

    def get_query_details(self, query_name: str) -> Dict[str, Any]:
        self.__check_query_existance(query_name)

        query = self.saved_queries[query_name]

        return {
            "name": query.name,
            "select_keys": query.select_keys,
            "sort_keys": query.sort_keys,
            "group_keys": query.group_keys,
            "filters": query.filters,
            "has_result": query.result is not None,
        }

    def __check_query_existance(self, query_name: str):
        if query_name not in self.saved_queries:
            raise ValueError(f"Query with name {query_name} not found")
