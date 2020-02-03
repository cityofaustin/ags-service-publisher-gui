from PyQt4 import QtGui
from PyQt4.QtCore import Qt

# Adapted from https://stackoverflow.com/a/43882058
class PlainTextEditWithPlaceholderText(QtGui.QPlainTextEdit):
    def __init__(self, parent=None):
        super(PlainTextEditWithPlaceholderText, self).__init__(parent)
        self.placeholderText = ''

    def setPlaceholderText(self, text):
        self.placeholderText = text

    def paintEvent(self, event):
        """
        Implements the same behavior as QLineEdit's setPlaceholderText()
        Draw the placeholder text when there is no text entered.
        """
        document = self.document()
        if self.placeholderText and document.isEmpty():
            offset = self.contentOffset()
            viewport = self.viewport()
            painter = QtGui.QPainter(viewport)
            painter.setBrushOrigin(offset)

            color = self.palette().text().color()
            color.setAlpha(128)
            painter.setPen(color)

            margin = int(document.documentMargin())
            text_rect = viewport.rect().adjusted(margin, margin, 0, 0)
            painter.drawText(text_rect, Qt.AlignTop | Qt.TextWordWrap, self.placeholderText)

            if (self.hasFocus()):
                context = self.getPaintContext()
                cursor_position = context.cursorPosition
                if cursor_position == -1:
                    # Cursor blinking means we don't need to draw it on this event
                    pass
                else:
                    block = self.firstVisibleBlock()
                    block_position = block.position()
                    layout = block.layout()
                    if cursor_position < -1:
                        cursor_position = layout.preeditAreaPosition() - (cursor_position + 2)
                    else:
                        cursor_position -= block_position
                    layout.drawCursor(painter, offset, cursor_position, self.cursorWidth())

            viewport.update()
        else:
            super(PlainTextEditWithPlaceholderText, self).paintEvent(event)
