import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QTextEdit, QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt

class StatsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.df = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #000000; font-family: Consolas, monospace; }
            QLabel { color: #00FF00; }
            QComboBox, QTableWidget, QTextEdit { background-color: #000000; color: #00FF00; border: 1px solid #00FF00; font-size: 14px; padding: 4px; }
            QPushButton { background-color: #000000; color: #00FF00; padding: 6px 12px; border: 1px solid #00FF00; border-radius: 4px; }
            QPushButton:hover { background-color: #005500; }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Data Statistics")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # Add a Refresh Stats button at the top
        self.btn_refresh = QPushButton("Refresh Stats")
        self.btn_refresh.clicked.connect(self.update_stats_view)
        layout.addWidget(self.btn_refresh)

        self.stats_summary = QTextEdit()
        self.stats_summary.setReadOnly(True)
        layout.addWidget(self.stats_summary)

        pair_layout = QHBoxLayout()
        self.combo_group = QComboBox()
        self.combo_target = QComboBox()
        pair_layout.addWidget(QLabel("Group by:"))
        pair_layout.addWidget(self.combo_group)
        pair_layout.addWidget(QLabel("Target:"))
        pair_layout.addWidget(self.combo_target)
        self.btn_compute = QPushButton("Compute Grouped Stats")
        self.btn_compute.clicked.connect(self.compute_group_stats)
        pair_layout.addWidget(self.btn_compute)
        layout.addLayout(pair_layout)

        self.stats_table = QTableWidget()
        layout.addWidget(self.stats_table)

        self.setLayout(layout)
        # Initially update view (if data available)
        self.update_stats_view()

    def update_stats_view(self):
        # Debug: print parent's df details.
        if self.parent.df is not None:
            print("StatsPage: Data loaded. DataFrame shape:", self.parent.df.shape)
            self.df = self.parent.df
            desc = self.df.describe(include="all")
            self.stats_summary.setPlainText(desc.to_string())
            columns = list(self.df.columns)
            self.combo_group.clear()
            self.combo_target.clear()
            self.combo_group.addItems(columns)
            self.combo_target.addItems(columns)
        else:
            print("StatsPage: No data loaded (self.parent.df is None)")
            self.stats_summary.setPlainText("No data loaded.")

    def compute_group_stats(self):
        if self.df is None:
            return
        group_col = self.combo_group.currentText()
        target_col = self.combo_target.currentText()
        try:
            group_stats = self.df.groupby(group_col)[target_col].agg(["mean", "sum", "max", "min"]).reset_index()
            self.populate_table(group_stats)
        except Exception as e:
            self.stats_summary.setPlainText(f"Error: {e}")

    def populate_table(self, df_table: pd.DataFrame):
        self.stats_table.clear()
        self.stats_table.setRowCount(len(df_table))
        self.stats_table.setColumnCount(len(df_table.columns))
        self.stats_table.setHorizontalHeaderLabels(df_table.columns)
        for i, row in df_table.iterrows():
            for j, col in enumerate(df_table.columns):
                self.stats_table.setItem(i, j, QTableWidgetItem(str(row[col])))