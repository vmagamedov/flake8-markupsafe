from gettext import gettext
from markupsafe import Markup


def safe(value):
    return Markup("<script>{}</script>").format(value)


def safe_i18n(value):
    return Markup(gettext("<script>{}</script>")).format(value)


def unsafe(value):
    return Markup("<script>{}</script>".format(value))


def unsafe_i18n(value):
    return Markup(gettext("<script>{}</script>".format(value)))
