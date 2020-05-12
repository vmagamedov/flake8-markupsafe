import ast
from typing import Tuple, List


def _named_call(call):
    return isinstance(call.func, ast.Name) or isinstance(call.func, ast.Attribute)


def _callable_name(call):
    if isinstance(call.func, ast.Name):
        return call.func.id
    elif isinstance(call.func, ast.Attribute):
        return call.func.attr
    else:
        raise TypeError(f"Unexpected type: {type(call.func)!r}")


def _is_i18n(name):
    return name in {"_", "N_"} or name.endswith("gettext")


def _arg_safe(arg):
    if isinstance(arg, ast.Str):
        return True
    elif (
        isinstance(arg, ast.Call) and _named_call(arg) and _is_i18n(_callable_name(arg))
    ):
        if len(arg.args) == 1:
            return isinstance(arg.args[0], ast.Str)
        else:
            # last argument is a number for a plural form
            return all(isinstance(a, ast.Str) for a in arg.args[:-1])
    else:
        return False


class PythonVisitor(ast.NodeVisitor):
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column
        self.locations: List[Tuple[int, int]] = []

    def visit_Call(self, node: ast.Call):
        if (
            _named_call(node)
            and _callable_name(node) in {"Markup", "literal"}
            and node.args
        ):
            if not _arg_safe(node.args[0]):
                self.locations.append(
                    (self.line + node.lineno, self.column + node.col_offset,)
                )
        self.generic_visit(node)
