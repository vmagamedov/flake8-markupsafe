import ast
from typing import Generator, Tuple, Type

from . import __version__
from .python import PythonVisitor


ErrorType = Tuple[int, int, str, Type]


class MarkupSafePlugin:
    name = "flake8-markupsafe"
    version = __version__

    def __init__(self, tree: ast.Module):
        self._tree = tree

    def run(self) -> Generator[ErrorType, None, None]:
        visitor = PythonVisitor()
        visitor.visit(self._tree)
        for lineno, col_offset in visitor.locations:
            yield (
                lineno,
                col_offset,
                "MS001 Markup is used in a dangerous way",
                type(self),
            )
