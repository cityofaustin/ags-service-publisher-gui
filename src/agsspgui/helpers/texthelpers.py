from xml.sax.saxutils import escape


def escape_html(text):
    return '<br>'.join(escape(str(text)).split('\n')).replace(' ', '&nbsp;')
