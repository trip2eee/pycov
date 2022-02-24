from PyQt5.QtWidgets import QMainWindow, QTextEdit
from PyQt5.QtGui import QColor, QTextBlockFormat, QTextCursor
from src.gcov_parser import *


class CodeWindow(QMainWindow):
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


        self.setCentralWidget(self.text_edit)
