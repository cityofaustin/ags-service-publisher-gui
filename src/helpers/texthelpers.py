from xml.sax.saxutils import escape


def escape_html(text):
    return escape(text)
