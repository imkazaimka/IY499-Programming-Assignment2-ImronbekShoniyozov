from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QComboBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import graphs

class ChartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()
        
        # Form layout for chart options: chart type and column selection
        form_layout = QFormLayout()
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Bar Chart", "Pie Chart", "Histogram", "Line Chart", "Scatter Plot"])
        form_layout.addRow("Chart Type:", self.chart_type_combo)
        
        self.column_combo = QComboBox()
        form_layout.addRow("Select Column:", self.column_combo)
        layout.addLayout(form_layout)
        
        # Button to generate the chart
        btn_plot = QPushButton("Generate Chart")
        btn_plot.clicked.connect(self.generate_chart)
        layout.addWidget(btn_plot)
        
        # Matplotlib canvas to display the generated figure
        self.canvas = FigureCanvas(graphs.create_empty_figure())
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
    def update_columns(self):
        """Refresh the column selection based on the loaded DataFrame."""
        self.column_combo.clear()
        if self.parent.df is not None:
            self.column_combo.addItems(self.parent.df.columns.tolist())
    
    def generate_chart(self):
        """Generate the selected chart and update the canvas."""
        if self.parent.df is None:
            return
        chart_type = self.chart_type_combo.currentText()
        column = self.column_combo.currentText()
        fig = None
        
        if chart_type == "Bar Chart":
            fig = graphs.plot_bar_chart(self.parent.df, column)
        elif chart_type == "Pie Chart":
            fig = graphs.plot_pie_chart(self.parent.df, column)
        elif chart_type == "Histogram":
            fig = graphs.plot_histogram(self.parent.df, column)
        elif chart_type == "Line Chart":
            fig = graphs.plot_line_chart(self.parent.df, column)
        elif chart_type == "Scatter Plot":
            fig = graphs.plot_scatter_plot(self.parent.df, column)
            
        if fig:
            self.canvas.figure = fig
            self.canvas.draw()
