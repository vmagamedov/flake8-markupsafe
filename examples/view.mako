<%
    valid = Markup('<script>{}</script>').format(value)
    invalid = Markup('<script>{}</script>' % value)
    ignored = Markup('<script>{}</script>' % value)  # noqa
%>
<div>
    <div>${Markup('<script>{}</script>').format(value)}</div>
    <div>${Markup('<script>%s</script>' % value)}</div>
    <div>${Markup('<script>{}</script>'.format(value))}</div>
    <div>${helpers.Markup('<script>{}</script>'.format(value))}</div>
</div>
