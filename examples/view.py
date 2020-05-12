import markupsafe
from markupsafe import Markup


def valid(value):
    return Markup("<script>{}</script>").format(value)


def valid_multiline(value):
    return Markup(
        """
        <script>{}</script>
        """
    ).format(value)


def dangerous_format_old(value):
    return Markup("<script>%s</script>" % value)


def dangerous_format_new(value):
    return Markup("<script>{}</script>".format(value))


def dangerous_fstring(value):
    return Markup(f"<script>{value}</script>")


def dangerous_as_attr(value):
    return markupsafe.Markup(f"<script>{value}</script>")
