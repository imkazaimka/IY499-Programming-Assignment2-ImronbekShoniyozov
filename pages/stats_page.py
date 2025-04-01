from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

class StatsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()
        
        # Text area to display statistics
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        layout.addWidget(self.stats_text)
        
        # Button to refresh statistics
        btn_refresh = QPushButton("Refresh Stats")
        btn_refresh.clicked.connect(self.update_stats)
        layout.addWidget(btn_refresh)
        
        self.setLayout(layout)
        
    def update_stats(self):
        if self.parent.df is not None:
            try:
                stats = self.parent.df.describe().to_string()
                self.stats_text.setPlainText(stats)
            except Exception as e:
                self.stats_text.setPlainText(f"Error computing stats: {e}")
        else:
            self.stats_text.setPlainText("No data loaded.")
