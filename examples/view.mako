<%
    safe = Markup('<script>{}</script>').format(value)
    unsafe = Markup('<script>{}</script>'.format(value))
    ignored = Markup('<script>{}</script>'.format(value))  # noqa
%>
<div>
    <div class="safe">${Markup('<script>{}</script>').format(value)}</div>
    <div class="unsafe">${Markup('<script>{}</script>'.format(value))}</div>
</div>
