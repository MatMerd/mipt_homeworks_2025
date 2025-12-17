from __future__ import annotations


def range_term(field: str, min_value: int, max_value: int | None) -> str | None:
    if max_value is not None:
        return f"{field}:{min_value}..{max_value}"
    if min_value > 0:
        return f"{field}:>={min_value}"
    return None


def build_github_query(
    *,
    lang: str,
    stars_min: int = 0,
    stars_max: int | None = None,
    forks_min: int = 0,
    forks_max: int | None = None,
) -> str:
    query_parts = [f"language:{lang}"]
    stars = range_term("stars", stars_min, stars_max)
    if stars:
        query_parts.append(stars)
    forks = range_term("forks", forks_min, forks_max)
    if forks:
        query_parts.append(forks)
    return " ".join(query_parts)
