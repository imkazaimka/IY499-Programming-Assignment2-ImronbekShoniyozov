from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from PySide6.QtCore import Qt

class TablePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Reference to MainWindow
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #000000; color: #00FF00; font-family: Consolas, monospace; }
            QTableWidget { background-color: #000000; color: #00FF00; gridline-color: #00FF00; }
            QHeaderView::section { background-color: #000000; color: #00FF00; }
            QPushButton { background-color: #000000; color: #00FF00; border: 1px solid #00FF00; padding: 6px; }
            QPushButton:hover { background-color: #005500; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Data Table")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.btn_refresh = QPushButton("Refresh Table")
        self.btn_refresh.clicked.connect(self.update_table)
        layout.addWidget(self.btn_refresh)

    def update_table(self):
        if self.parent.df is None:
            return
        df = self.parent.df
        self.table.clear()
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(list(df.columns))
        for i, row in df.iterrows():
            for j, col in enumerate(df.columns):
                self.table.setItem(i, j, QTableWidgetItem(str(row[col])))