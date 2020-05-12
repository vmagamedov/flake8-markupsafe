import ast
import textwrap

import pytest

from flake8_markupsafe.python import PythonVisitor


@pytest.fixture(name="code")
def code_fixture(request):
    return ast.parse(textwrap.dedent(request.function.__doc__))


def check(code):
    visitor = PythonVisitor()
    visitor.visit(code)
    return visitor.locations


def test_safe(code):
    """
    Markup("<script>{}</script>").format(value)
    """
    assert not check(code)


@pytest.mark.parametrize("argument", ["1", "1.1", "True", "False", "None"])
def test_scalars(argument):
    assert not check(ast.parse(f"literal({argument})"))


def test_empty(code):
    """
    Markup()
    """
    assert not check(code)


def test_unsafe(code):
    """
    Markup("<script>{}</script>".format(value))
    """
    assert check(code)


def test_unsafe_percent(code):
    """
    Markup("<script>%s</script>" % value)
    """
    assert check(code)


def test_unsafe_fstring(code):
    """
    Markup(f"<script>{value}</script>")
    """
    assert check(code)


def test_attr_safe(code):
    """
    ns.Markup(_("<script>{}</script>")).format(value)
    """
    assert not check(code)


def test_attr_unsafe(code):
    """
    ns.Markup(_("<script>{}</script>").format(value))
    """
    assert check(code)


def test_gettext_safe(code):
    """
    Markup(gettext("<script>{}</script>")).format(value)
    """
    assert not check(code)


def test_gettext_unsafe(code):
    """
    Markup(gettext("<script>{}</script>".format(value)))
    """
    assert check(code)


def test_gettext_unsafe2(code):
    """
    Markup(gettext("<script>{}</script>").format(value))
    """
    assert check(code)


def test_ngettext_safe(code):
    """
    Markup(ngettext("single", "plural", count))
    """
    assert not check(code)


def test_ngettext_unsafe(code):
    """
    Markup(ngettext("single", "plural".format(value), count))
    """
    assert check(code)


def test_custom_ngettext_safe(code):
    """
    Markup(custom_ngettext("single", "plural", "special", count))
    """
    assert not check(code)


def test_custom_ngettext_unsafe(code):
    """
    Markup(custom_ngettext("single", "plural", "special".format(value), count))
    """
    assert check(code)
