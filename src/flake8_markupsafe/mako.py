import os
import sys
import codecs
import argparse
import textwrap

from mako import pyparser
from mako.lexer import Lexer

from .python import PythonVisitor


class MakoVisitor:
    def __init__(self):
        self.locations = []

    def visitCode(self, node):
        expr = pyparser.parse(textwrap.dedent(node.code.code))
        visitor = PythonVisitor(node.lineno - 1, node.pos)
        visitor.visit(expr)
        self.locations.extend(visitor.locations)

    def visitExpression(self, node):
        self.visitCode(node)


def _mako_file_check(filename, show_source):
    with codecs.open(filename, "rb", "utf-8") as f:
        text = f.read()
    lexer = Lexer(text, filename)
    visitor = MakoVisitor()
    node = lexer.parse()
    node.accept_visitor(visitor)
    if visitor.locations:
        text_lines = text.splitlines()
        for line, _ in visitor.locations:
            if not text_lines[line - 1].endswith("# noqa"):
                print(f"{filename}:{line}")
                if show_source:
                    print(f"    {text_lines[line - 1].lstrip()}")
    return bool(visitor.locations)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--show-source", action="store_true")
    namespace = parser.parse_args()

    failed = False
    if os.path.isdir(namespace.path):
        for dirpath, dirnames, filenames in os.walk(namespace.path):
            for filename in filenames:
                if filename.endswith(".mako"):
                    failed = (
                        _mako_file_check(
                            os.path.join(dirpath, filename), namespace.show_source
                        )
                        or failed
                    )
    elif os.path.isfile(namespace.path):
        failed = _mako_file_check(namespace.path, namespace.show_source)
    else:
        print(f"Wrong files path: {namespace.path}", file=sys.stderr)
        sys.exit(2)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
