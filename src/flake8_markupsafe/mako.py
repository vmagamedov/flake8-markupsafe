import os
import argparse

from mako import pyparser
from mako.lexer import Lexer

from .python import PythonVisitor


class MakoVisitor:
    def __init__(self):
        self.locations = []

    def visitExpression(self, node):
        expr = pyparser.parse(node.code.code.lstrip())
        visitor = PythonVisitor(node.lineno, node.pos)
        visitor.visit(expr)
        self.locations.extend(visitor.locations)

    def visitCode(self, node):
        self.visitExpression(node)


def _mako_file_check(filename):
    with open(filename, "rb") as f:
        text = f.read()
    lexer = Lexer(text, filename)
    visitor = MakoVisitor()
    node = lexer.parse()
    node.accept_visitor(visitor)
    if visitor.locations:
        text_lines = text.splitlines()
        for line, _ in visitor.locations:
            if not text_lines[line - 1].endswith(b"# noqa"):
                print(f"{filename}:{line}")


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    namespace = parser.parse_args()
    for dirpath, dirnames, filenames in os.walk(namespace.path):
        for filename in filenames:
            if filename.endswith(".mako"):
                _mako_file_check(os.path.join(dirpath, filename))


if __name__ == "__main__":
    _main()
