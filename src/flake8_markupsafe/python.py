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
        return _args_safe(arg.args)
    else:
        return False


def _args_safe(args):
    if len(args) == 1:
        return _arg_safe(args[0])
    elif len(args) in (3, 4):
        # last argument is a number for a ngettext-like function
        return all(_arg_safe(arg) for arg in args[:-1])
    else:
        raise ValueError("Wrong number of arguments")


class PythonVisitor(ast.NodeVisitor):
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column
        self.locations: List[Tuple[int, int]] = []

    def visit_Call(self, node: ast.Call):
        if _named_call(node) and _callable_name(node) in {"Markup", "literal"}:
            assert len(node.args) == 1, ast.dump(node)
            if not _arg_safe(node.args[0]):
                self.locations.append(
                    (self.line + node.lineno, self.column + node.col_offset)
                )
        self.generic_visit(node)
