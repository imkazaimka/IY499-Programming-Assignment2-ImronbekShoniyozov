import numpy as np
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QComboBox, QPushButton, 
    QHBoxLayout, QLabel
)
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, 
    QLineSeries, QScatterSeries, QPieSeries, QValueAxis
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

def get_bar_data(df, column):
    counts = df[column].value_counts()
    return {"categories": list(map(str, counts.index)), "counts": counts.values.tolist()}

def get_pie_data(df, column):
    counts = df[column].value_counts()
    return {"labels": list(map(str, counts.index)), "values": counts.values.tolist()}

def get_histogram_data(df, column, bins=10):
    # Convert to numeric (drop non-numeric)
    numeric_series = pd.to_numeric(df[column].dropna(), errors='coerce').dropna()
    values = numeric_series.values
    if values.size == 0:
        return {"bins": [], "counts": []}
    counts, bin_edges = np.histogram(values, bins=bins)
    labels = [f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}" for i in range(len(bin_edges)-1)]
    return {"bins": labels, "counts": counts.tolist()}

def get_line_data(df, column):
    numeric_series = pd.to_numeric(df[column].dropna(), errors='coerce').dropna().tolist()
    return {"x": list(range(len(numeric_series))), "y": numeric_series}

def get_scatter_data(df, column):
    numeric_series = pd.to_numeric(df[column].dropna(), errors='coerce').dropna().tolist()
    return {"x": list(range(len(numeric_series))), "y": numeric_series}

class GraphsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        # Connect graph type change to update axis controls.
        self.combo_graph_type.currentIndexChanged.connect(self.update_axis_controls)

    def init_ui(self):
        # Fallout style: black background and bright green text.
        self.setStyleSheet("""
            QWidget { background-color: #000000; color: #00FF00; font-family: Consolas, monospace; }
            QLabel { color: #00FF00; }
            QComboBox { background-color: #000000; color: #00FF00; border: 1px solid #00FF00; padding: 4px; }
            QPushButton { background-color: #000000; color: #00FF00; border: 1px solid #00FF00; padding: 6px 12px; }
            QPushButton:hover { background-color: #005500; }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Graph Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # Form Layout for graph type selection and axis controls.
        self.form_layout = QFormLayout()
        self.combo_graph_type = QComboBox()
        self.combo_graph_type.addItems(["Bar Chart", "Line Chart", "Scatter Chart", "Histogram", "Pie Chart"])
        self.form_layout.addRow("Graph Type:", self.combo_graph_type)
        
        # For some graphs only one axis is needed; we'll use combo_column_x for that.
        self.combo_column_x = QComboBox()
        self.label_column_x = QLabel("Column:")
        self.form_layout.addRow(self.label_column_x, self.combo_column_x)

        # For graphs that need two axes, show combo_column_y.
        self.combo_column_y = QComboBox()
        self.label_column_y = QLabel("Y-Axis Column:")
        self.form_layout.addRow(self.label_column_y, self.combo_column_y)

        layout.addLayout(self.form_layout)

        btn_layout = QHBoxLayout()
        self.btn_generate = QPushButton("Generate Graph")
        self.btn_generate.clicked.connect(self.generate_graph)
        btn_layout.addWidget(self.btn_generate)
        layout.addLayout(btn_layout)

        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout()
        self.chart_container.setLayout(self.chart_layout)
        layout.addWidget(self.chart_container)

        self.setLayout(layout)
        # Initially update axis controls based on the default graph type.
        self.update_axis_controls()

    def update_axis_controls(self):
        """
        Update the axis controls based on selected graph type.
        For Bar Chart, Histogram, and Pie Chart, only one column is required.
        For Line Chart and Scatter Chart, show both column selections.
        """
        graph_type = self.combo_graph_type.currentText()
        if graph_type in ["Bar Chart", "Histogram", "Pie Chart"]:
            # Hide Y-Axis column controls
            self.label_column_y.hide()
            self.combo_column_y.hide()
            # Optionally, change label for X-Axis to "Value/Category" if needed.
            if graph_type == "Bar Chart":
                self.label_column_x.setText("Category:")
            elif graph_type == "Histogram":
                self.label_column_x.setText("Numeric Column:")
            elif graph_type == "Pie Chart":
                self.label_column_x.setText("Category:")
        else:
            # Show both controls for graphs requiring two axes.
            self.label_column_y.show()
            self.combo_column_y.show()
            self.label_column_x.setText("X-Axis Column:")

    def update_columns(self):
        if self.parent.df is not None:
            cols = list(self.parent.df.columns)
            self.combo_column_x.clear()
            self.combo_column_y.clear()
            self.combo_column_x.addItems(cols)
            self.combo_column_y.addItems(cols)

    def clear_chart_view(self):
        if self.chart_container.layout().count() > 0:
            old_widget = self.chart_container.layout().itemAt(0).widget()
            if old_widget:
                self.chart_container.layout().removeWidget(old_widget)
                old_widget.deleteLater()

    def generate_graph(self):
        if self.parent.df is None:
            return
        self.clear_chart_view()
        graph_type = self.combo_graph_type.currentText()
        # For one-axis graphs, use combo_column_x only.
        # For two-axis graphs, use both.
        if graph_type in ["Bar Chart", "Histogram", "Pie Chart"]:
            x_col = self.combo_column_x.currentText()
            y_col = None
        else:
            x_col = self.combo_column_x.currentText()
            y_col = self.combo_column_y.currentText()
        df = self.parent.df

        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # Set chart title depending on the selected graph and axes.
        if y_col:
            chart.setTitle(f"{graph_type} ({x_col} vs {y_col})")
        else:
            chart.setTitle(f"{graph_type} ({x_col})")

        if graph_type == "Bar Chart":
            data = get_bar_data(df, x_col)
            # In a bar chart, the chosen column is used for category,
            # and we use a default value for the bars. Here, we simply use the counts.
            bar_set = QBarSet("Count")
            bar_set.append(data["counts"])
            series = QBarSeries()
            series.append(bar_set)
            chart.addSeries(series)
            axis_x = QBarCategoryAxis()
            axis_x.append(data["categories"])
            chart.addAxis(axis_x, Qt.AlignBottom)
            series.attachAxis(axis_x)
            axis_y = QValueAxis()
            if data["counts"]:
                axis_y.setRange(0, max(data["counts"]) * 1.1)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_y)

        elif graph_type == "Histogram":
            data = get_histogram_data(df, x_col, bins=10)
            if not data["bins"]:
                chart.setTitle(f"Histogram for {x_col} - No Numeric Data Found")
            else:
                bar_set = QBarSet("Frequency")
                bar_set.append(data["counts"])
                series = QBarSeries()
                series.append(bar_set)
                chart.addSeries(series)
                axis_x = QBarCategoryAxis()
                axis_x.append(data["bins"])
                chart.addAxis(axis_x, Qt.AlignBottom)
                series.attachAxis(axis_x)
                axis_y = QValueAxis()
                axis_y.setRange(0, max(data["counts"]) * 1.1)
                chart.addAxis(axis_y, Qt.AlignLeft)
                series.attachAxis(axis_y)

        elif graph_type == "Pie Chart":
            grouped = df.groupby(x_col).sum().reset_index()  # For simplicity, summing all numeric columns.
            # Use x_col as category and use the sum for the first numeric column found.
            numeric_cols = [col for col in grouped.columns if pd.api.types.is_numeric_dtype(grouped[col]) and col != x_col]
            if not numeric_cols:
                chart.setTitle(f"Pie Chart for {x_col} - No Numeric Data Found")
            else:
                target = numeric_cols[0]
                labels = list(grouped[x_col].astype(str))
                values = list(grouped[target])
                series = QPieSeries()
                for label, value in zip(labels, values):
                    series.append(label, value)
                chart.addSeries(series)
                chart.legend().setAlignment(Qt.AlignBottom)

        elif graph_type == "Line Chart":
            data = get_line_data(df, y_col)
            series = QLineSeries()
            for x, y in zip(data["x"], data["y"]):
                series.append(x, y)
            chart.addSeries(series)
            chart.createDefaultAxes()

        elif graph_type == "Scatter Chart":
            data = get_scatter_data(df, y_col)
            series = QScatterSeries()
            for x, y in zip(data["x"], data["y"]):
                series.append(x, y)
            chart.addSeries(series)
            chart.createDefaultAxes()

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_layout.addWidget(self.chart_view)