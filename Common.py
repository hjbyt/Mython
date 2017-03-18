from typing import NamedTuple


class CompilationError(ValueError):
    pass


class Position(NamedTuple):
    line_number: int
    column: int
