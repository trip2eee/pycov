import os

from PyQt5.QtWidgets import QMainWindow, QAction, qApp
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.QtWidgets import QProgressBar, QFileDialog
from PyQt5.QtCore import QSize

from src.gcov_parser import GCOVParser


class MainWindow(QMainWindow):
    """ PyCov Main window class
    """
    def __init__(self, argv) -> None:
        super().__init__()

        self.initUI()

        self.path = './'
        self.open_folder(self.path)

    def initUI(self):                
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')

        actionOpen = QAction('&Open Folder', self)
        actionOpen.setShortcut('Ctrl+O')
        actionOpen.triggered.connect(self.event_open_folder)
        file_menu.addAction(actionOpen)

        actionRefresh = QAction('&Refresh', self)
        actionRefresh.setShortcut('Ctrl+R')
        actionRefresh.triggered.connect(self.event_refresh)
        file_menu.addAction(actionRefresh)

        file_menu.addSeparator()

        actionExit = QAction('E&xit', self)
        actionExit.setShortcut('Ctrl+Q')
        actionExit.triggered.connect(qApp.quit)
        file_menu.addAction(actionExit)

        self.file_tree = QTreeWidget()
        self.file_tree.setColumnCount(4)
        self.file_tree.setHeaderLabels(['File Path', 'Line Coverage', 'Functions', 'Branches', ''])
        self.file_tree.header().resizeSection(0, 300)
        self.file_tree.header().resizeSection(4, 0)
        self.file_tree.itemDoubleClicked.connect(self.event_item_double_clicked)
        self.setCentralWidget(self.file_tree)

        self.setWindowTitle('PyCov')
        self.resize(QSize(800, 500))

    def event_open_folder(self):
        """ File -> Open menu event handler.
        """
        open_path = QFileDialog.getExistingDirectory(self, "Select Directory")

        if open_path != '':
            self.path = open_path
            self.open_folder(self.path)
    
    def event_refresh(self):
        """ File -> Refresh menu event handler.
        """
        self.open_folder(self.path)

    def event_item_double_clicked(self):
        """ file_tree (QTreeWidget) itemDoubleClicked event handler.
            This method is called when an item of file_tree is double clicked.
        """
        pass

    def add_progressbar(self, item, idx_col, value):
        """ This method add a progressbar in the specific column of the input item.
            item: [in] The item in which a progressbar is added.
            idx_col: [in] The specific column in which a progressbar is added.
            value: [in] The value of the progressbar to be added. unit:%
                        The color of progressbar is determined based on the value.
                        - value >= 90: green
                        - value >= 80: yellow
                        - value < 80: red
        """
        bar = QProgressBar(self)
        bar.setRange(0, 100)
        bar.setValue(value)
        bar.setMinimumWidth(10)

        if value >= 90:
            color = 'lightgreen'
        elif value >= 80:
            color = 'yellow'
        else:
            color = 'red'

        bar.setStyleSheet(
                        "QProgressBar"
                        "{text-align: center; background-color: transparent; border: 1px solid transparent;}"
                        "QProgressBar:chunk"
                        "{background-color: " + color + "; border-radius: 3px;}"
                        )
        self.file_tree.setItemWidget(item, idx_col, bar)

    def open_folder(self, path):
        
        list_files = os.scandir(path)
        self.list_cov = []

        self.num_lines = 0
        self.num_lines_exec = 0

        self.num_branches = 0
        self.num_branches_exec = 0

        self.num_functions = 0
        self.num_functions_exec = 0

        for file in list_files:
            if file.name.endswith('.gcov'):
                print(file.path)

                cov = GCOVParser(file.path)
                self.list_cov.append(cov)

                self.num_lines += cov.num_lines
                self.num_lines_exec += cov.num_lines_exec

                self.num_branches += cov.num_branches
                self.num_branches_exec += cov.num_branches_exec

                self.num_functions += cov.num_functions
                self.num_functions_exec += cov.num_functions_exec

        if self.num_lines > 0:
            self.line_coverage = self.num_lines_exec / self.num_lines
        else:
            self.line_coverage = 1.0

        if  self.num_functions > 0:
            self.function_coverage = self.num_functions_exec / self.num_functions
        else:
            self.function_coverage = 1.0

        if self.num_branches > 0:
            self.branch_coverage = self.num_branches_exec / self.num_branches
        else:
            self.branch_coverage = 1.0

        self.file_tree.clear()

        items = []
        for i in range(len(self.list_cov)):
            item = QTreeWidgetItem()
            item.setText(0, self.list_cov[i].file_path)            
            items.append(item)
        
        item_total = QTreeWidgetItem()
        item_total.setText(0, 'Total')
        items.append(item_total)
        self.file_tree.insertTopLevelItems(0, items)

        it = QTreeWidgetItemIterator(self.file_tree)
        while it.value():
            
            idx_item = self.file_tree.indexOfTopLevelItem(it.value())
            if idx_item < len(self.list_cov):
                lines = self.list_cov[idx_item].line_coverage
                branch = self.list_cov[idx_item].branch_coverage
                function = self.list_cov[idx_item].function_coverage
            else:
                lines = self.line_coverage
                branch = self.branch_coverage
                function = self.function_coverage

            self.add_progressbar(it.value(), 1, int(lines * 100))
            self.add_progressbar(it.value(), 2, int(function * 100))
            self.add_progressbar(it.value(), 3, int(branch * 100))

            it += 1

