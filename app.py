import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QToolBar, QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt

from pages.home_page import HomePage
from pages.stats_page import StatsPage  # If still needed; otherwise, remove
from pages.graphs_page import GraphsPage
from pages.table_page import TablePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimalistic Data Analytics App")
        self.resize(1200, 800)
        self.df = None  # Shared DataFrame

        # Create a stacked widget and pages
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage(self)  # Home page with file browsing etc.
        self.stats_page = StatsPage(self)  # Statistics page; optional if you prefer
        self.graphs_page = GraphsPage(self)  # Graphs page using Qt Charts
        self.table_page = TablePage(self)    # New Table page showing data

        self.stack.addWidget(self.home_page)   # index 0
        self.stack.addWidget(self.stats_page)    # index 1
        self.stack.addWidget(self.graphs_page)   # index 2
        self.stack.addWidget(self.table_page)    # index 3

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar { background-color: #000000; border: none; }
            QPushButton { background-color: #000000; color: #00FF00; border: none; padding: 8px 12px; }
            QPushButton:hover { background-color: #005500; }
        """)
        
        home_btn = QPushButton("Home")
        home_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.home_page))
        stats_btn = QPushButton("Statistics")
        stats_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.stats_page))
        graphs_btn = QPushButton("Graphs")
        graphs_btn.clicked.connect(lambda: self.graphs_page.update_columns() or self.stack.setCurrentWidget(self.graphs_page))
        table_btn = QPushButton("Table")
        table_btn.clicked.connect(lambda: self.table_page.update_table() or self.stack.setCurrentWidget(self.table_page))
        
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(home_btn)
        layout.addWidget(stats_btn)
        layout.addWidget(graphs_btn)
        layout.addWidget(table_btn)
        container = QWidget()
        container.setLayout(layout)
        toolbar.addWidget(container)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())