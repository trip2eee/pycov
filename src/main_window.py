import PyQt5
from PyQt5.QtWidgets import QMainWindow, QAction, qApp
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):
    """ PyCov Main window class
    """
    def __init__(self, argv) -> None:
        super().__init__()

        self.initUI()

        self.open_folder('')

    def initUI(self):                
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')

        actionOpen = QAction('Open Folder', self)
        actionOpen.setShortcut('Ctrl+O')
        file_menu.addAction(actionOpen)

        file_menu.addSeparator()

        actionExit = QAction('Exit', self)
        actionExit.setShortcut('Ctrl+Q')
        actionExit.triggered.connect(qApp.quit)
        file_menu.addAction(actionExit)

        self.list_file = QTreeWidget()
        self.list_file.setColumnCount(4)
        self.list_file.setHeaderLabels(['File Path', 'Line Coverage', 'Functions', 'Branches', ''])
        self.list_file.header().resizeSection(0, 200)
        self.list_file.header().resizeSection(4, 0)
        
        self.setCentralWidget(self.list_file)

        self.setWindowTitle('PyCov')
        self.resize(QSize(600, 300))

    def event_open_folder(self):
        pass


    def add_progressbar(self, item, idx_col, value, color):
        bar = QProgressBar(self)
        bar.setRange(0, 100)
        bar.setValue(value)
        bar.setMinimumWidth(10)

        bar.setStyleSheet(
                        "QProgressBar"
                        "{text-align: center; background-color: transparent; border: 1px solid transparent;}"
                        "QProgressBar:chunk"
                        "{background-color: " + color + "; border-radius: 3px;}"
                        )
        self.list_file.setItemWidget(item, idx_col, bar)

    def open_folder(self, path):
        items = []

        for i in range(5):
            item = QTreeWidgetItem(i)
            item.setText(0, 'File ' + str(i))            
            items.append(item)
        
        self.list_file.insertTopLevelItems(0, items)

        it = QTreeWidgetItemIterator(self.list_file)
        while it.value():
            self.add_progressbar(it.value(), 1, 80, 'lightgreen')
            self.add_progressbar(it.value(), 2, 70, 'yellow')
            self.add_progressbar(it.value(), 3, 60, 'red')

            it += 1


        