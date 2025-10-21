from entity.group_type import GroupType
from entity.sort_type import SortType


class Request:
    def __init__(self, sort_by: list[SortType], group_by: list[GroupType]):
        self.sort_by = sort_by
        self.group_by = group_by
