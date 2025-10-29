from dataclasses import dataclass, field
from typing import List, Any
from enum import Enum


class OperationType(Enum):
    """Типы операций"""
    SORT = 1
    SELECT = 2
    GROUP_BY = 3
    WHERE = 4
    LIMIT = 5

@dataclass
class Operation:
    operation_type: OperationType
    args: List[Any] = field(default_factory=list)

@dataclass
class Query:
    operations: List[Operation] = field(default_factory=list)
    result: Any = None
    
@dataclass
class QueryStats:
    median: int 
    most_liked_repo: dict[str, Any]
    longest_name_repo: dict[str, Any]
    no_lang_repos: list[dict[str, Any]]
    top_no_commits_repos: list[dict[str, Any]]  # no = number of