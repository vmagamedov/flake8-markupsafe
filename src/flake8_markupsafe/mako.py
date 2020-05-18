import os
import sys
import codecs
import argparse
import textwrap
from gettext import ngettext

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
    count = 0
    if visitor.locations:
        text_lines = text.splitlines()
        for line, _ in visitor.locations:
            if not text_lines[line - 1].endswith("# noqa"):
                print(f"{filename}:{line}")
                if show_source:
                    print(f"    {text_lines[line - 1].lstrip()}")
                count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--show-source", action="store_true")
    namespace = parser.parse_args()

    errors_count = 0
    files_count = 0
    if os.path.isdir(namespace.path):
        for dirpath, dirnames, filenames in os.walk(namespace.path):
            for filename in filenames:
                if filename.endswith(".mako"):
                    count = _mako_file_check(
                        os.path.join(dirpath, filename), namespace.show_source
                    )
                    if count:
                        errors_count += count
                        files_count += 1
    elif os.path.isfile(namespace.path):
        count = _mako_file_check(namespace.path, namespace.show_source)
        if count:
            errors_count += count
            files_count += 1
    else:
        print(f"Wrong files path: {namespace.path}", file=sys.stderr)
        sys.exit(2)

    if errors_count:
        print(
            f"Found {errors_count} {ngettext('error', 'errors', errors_count)}"
            f" in {files_count} {ngettext('file', 'files', files_count)}",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        print("No errors found", file=sys.stderr)


if __name__ == "__main__":
    main()
