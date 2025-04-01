import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QToolBar, QPushButton
from PySide6.QtCore import Qt

from pages.home_page import HomePage
from pages.stats_page import StatsPage
from pages.chart_page import ChartPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistical Analysis App")
        self.df = None  # Shared DataFrame across pages

        # Create a stacked widget to hold our pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Instantiate pages and add them to the stacked widget
        self.home_page = HomePage(self)
        self.stats_page = StatsPage(self)
        self.chart_page = ChartPage(self)
        self.stacked_widget.addWidget(self.home_page)   # index 0
        self.stacked_widget.addWidget(self.stats_page)    # index 1
        self.stacked_widget.addWidget(self.chart_page)    # index 2

        # Navigation toolbar at the bottom
        nav_widget = QWidget()
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)
        btn_home = QPushButton("Home")
        btn_home.clicked.connect(lambda: self.change_page(0))
        nav_layout.addWidget(btn_home)
        btn_stats = QPushButton("Statistics")
        btn_stats.clicked.connect(lambda: self.change_page(1))
        nav_layout.addWidget(btn_stats)
        btn_charts = QPushButton("Charts")
        btn_charts.clicked.connect(self.go_to_chart)
        nav_layout.addWidget(btn_charts)
        nav_widget.setLayout(nav_layout)

        self.addToolBar(Qt.BottomToolBarArea, self.create_toolbar(nav_widget))

    def create_toolbar(self, widget):
        toolbar = QToolBar()
        toolbar.addWidget(widget)
        return toolbar

    def change_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        # When switching to the chart page, update column choices
        if index == 2:
            self.chart_page.update_columns()

    def go_to_chart(self):
        self.chart_page.update_columns()
        self.change_page(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
