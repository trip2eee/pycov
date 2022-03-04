from PyQt5.QtWidgets import QMainWindow, QTextEdit, QWidget, QHBoxLayout
from PyQt5.QtGui import QColor, QTextBlockFormat, QTextCursor, QPainter
from src.gcov_parser import *


class NumberBar(QWidget):
    """ Reference: NumberBar from https://nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/
    """
    def __init__(self):
        super().__init__()

        self.edit = None        
        self.highest_line = 0      # the greatest line number that is currently visible.
    
    def setEdit(self, edit):
        self.edit = edit
    
    def update(self):
        """ This method updates number bar
        """

        # +10 for margin
        width = self.fontMetrics().width(str(self.highest_line)) + 10
        if self.width() != width:
            self.setFixedWidth(width)
    
        super().update()

    def paintEvent(self, event):
        contents_y = self.edit.verticalScrollBar().value()
        page_bottom = contents_y + self.edit.viewport().height()    # the height of viewport widget.
        font_metrics = self.fontMetrics()
        current_block = self.edit.document().findBlock(self.edit.textCursor().position())   # get the text block that contains the current cursor.

        painter = QPainter(self)

        line_count = 0
        block = self.edit.document().begin()
        while block.isValid():
            line_count += 1
            position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

            if position.y() > page_bottom:
                break

            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
            
            painter.drawText(self.width() - font_metrics.width(str(line_count)) - 5, round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))

            if bold:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)

            block = block.next()

        self.highest_line = line_count
        painter.end()

        super().paintEvent(event)

class CodeWindow(QMainWindow):
    """ Code view window.
    """
    def __init__(self, cov: GCOVParser) -> None:
        super().__init__()

        self.cov = cov
        self.initUI()

        
    def initUI(self):
        self.setWindowTitle(self.cov.file_path)        
        self.resize(800, 500)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setText('')

        self.number_bar = NumberBar()
        self.number_bar.setEdit(self.text_edit)

        self.hbox = QHBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.hbox)

        self.hbox.setSpacing(0)
        self.hbox.addWidget(self.number_bar)
        self.hbox.addWidget(self.text_edit)        
        self.setCentralWidget(self.widget)

        self.text_edit.installEventFilter(self)
        self.text_edit.viewport().installEventFilter(self)

        for line in self.cov.lines:
            color = QColor()
            fmt = QTextBlockFormat()
            if line.covered == Coverage.NONE:                
                color.setRgb(255, 204, 203)
            elif line.covered == Coverage.PARTIAL:
                color.setRgb(255, 255, 0)
            elif line.covered == Coverage.FULL:
                color.setRgb(144, 238, 144)
            else:                
                color.setRgb(255, 255, 255)
            
            
            self.text_edit.append(line.line)

            fmt.setBackground(color)            
            cursor = self.text_edit.textCursor()
            cursor.setBlockFormat(fmt)

        # Move to the first line.
        self.text_edit.moveCursor(QTextCursor.Start)
    
    def eventFilter(self, object, event):
        if object in (self.text_edit, self.text_edit.viewport()):
            self.number_bar.update()
            return False
        return super().eventFilter(object, event)
