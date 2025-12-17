from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationPlan:
    per_page: int
    start_page: int
    start_index: int
    need_total: int


def plan_pagination(*, limit: int, offset: int, per_page: int = 100) -> PaginationPlan:
    start_page = offset // per_page + 1
    start_index = offset % per_page
    need_total = start_index + limit
    return PaginationPlan(
        per_page=per_page,
        start_page=start_page,
        start_index=start_index,
        need_total=need_total,
    )
