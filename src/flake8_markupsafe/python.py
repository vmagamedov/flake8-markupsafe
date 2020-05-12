import ast
from typing import Tuple, List


FUNCTIONS = {
    "Markup",
    "literal",
}


class PythonVisitor(ast.NodeVisitor):
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column
        self.locations: List[Tuple[int, int]] = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in FUNCTIONS:
            assert len(node.args) == 1, ast.dump(node)
            arg = node.args[0]
            if not isinstance(arg, ast.Str):
                self.locations.append(
                    (self.line + node.lineno, self.column + node.col_offset,)
                )
        self.generic_visit(node)
