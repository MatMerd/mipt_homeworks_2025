from typing import Iterable


class FieldNotFoundError(KeyError):
    def __init__(self, field: str, candidates: Iterable[str]):
        self.field = field
        self.candidates = tuple(candidates)
        message = f"Unknown field: {field}. Did you mean: {', '.join(self.candidates)}"
        super().__init__(message)


class InvalidOperationError(Exception):
    pass
