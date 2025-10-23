from difflib import get_close_matches
from typing import Iterable


class FieldResolver:
    def __init__(self, available: Iterable[str]):
        items = list(available)
        self._available = set(items)
        self._lower_map = {x.lower(): x for x in items}

    def resolve(self, name: str) -> str:
        if name in self._available:
            return name
        lower = name.lower()
        if lower in self._lower_map:
            return self._lower_map[lower]
        close = get_close_matches(name, list(self._available), n=3, cutoff=0.6)
        raise KeyError(",".join(close))


def try_int(text: str) -> int | None:
    try:
        return int(text)
    except Exception:
        return None


def try_float(text: str) -> float | None:
    try:
        return float(text)
    except Exception:
        return None
