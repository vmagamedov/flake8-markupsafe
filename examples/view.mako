<%
    safe = Markup('<script>{}</script>').format(value)
    unsafe = Markup('<script>{}</script>'.format(value))
    ignored = Markup('<script>{}</script>'.format(value))  # noqa
    safe_capture = Markup(capture(some_def, value))
%>
<div>
    <div class="safe">${Markup('<script>{}</script>').format(value)}</div>
    <div class="unsafe">${Markup('<script>{}</script>'.format(value))}</div>
    <div class="ignored">${Markup('<script>{}</script>'.format(value))}</div><%doc>noqa</%doc>
    <div class="safe filter">${'value'|n}</div>
    <div class="unsafe filter">${value|n}</div>
</div>
