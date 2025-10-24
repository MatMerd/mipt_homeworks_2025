from entity.group_type import GroupType
from entity.sort_type import SortType
from entity.where_type import WhereType


class Request:
    def __init__(
            self,
            sort_by: list[SortType],
            group_by: set[GroupType],
            where_by: dict[WhereType, str]
    ):
        self.sort_by = sort_by
        self.group_by = group_by
        self.where_by = where_by
