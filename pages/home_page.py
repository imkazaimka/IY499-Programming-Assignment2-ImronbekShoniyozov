import os
import glob
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton,
    QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
import logic  # Your module for data I/O and normalization

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.default_folder = os.path.join(os.getcwd(), "data")
        self.init_ui()
        self.load_csv_file_list(self.default_folder)

    def init_ui(self):
        # Fallout theme: black background, bright green text, monospace font.
        self.setStyleSheet("""
            QWidget { 
                background-color: #000000; 
                font-family: Consolas, monospace; 
            }
            QLabel { 
                color: #00FF00; 
            }
            QListWidget { 
                background-color: #000000; 
                color: #00FF00; 
                border: 1px solid #00FF00; 
            }
            QPushButton { 
                background-color: #000000; 
                color: #00FF00; 
                padding: 8px 16px; 
                border: 1px solid #00FF00; 
                border-radius: 4px; 
            }
            QPushButton:hover { 
                background-color: #005500; 
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Welcome to Minimalistic Data Analytics")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        instruction = QLabel("Select a CSV file from the folder below to begin your analysis:")
        instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction)

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh File List")
        self.btn_refresh.clicked.connect(lambda: self.load_csv_file_list(self.default_folder))
        self.btn_browse = QPushButton("Browse Folder")
        self.btn_browse.clicked.connect(self.browse_folder)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_browse)
        layout.addLayout(btn_layout)

        self.btn_load = QPushButton("Load Selected File")
        self.btn_load.clicked.connect(self.load_selected_file)
        layout.addWidget(self.btn_load)

        self.setLayout(layout)

    def load_csv_file_list(self, folder):
        self.file_list.clear()
        self.default_folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        csv_files = glob.glob(os.path.join(folder, "*.csv"))
        if not csv_files:
            self.file_list.addItem("No CSV files found in the folder.")
        else:
            for file in csv_files:
                self.file_list.addItem(file)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select CSV Folder", os.getcwd())
        if folder:
            self.load_csv_file_list(folder)

    def load_selected_file(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select a CSV file from the list.")
            return
        file_path = selected_item.text()
        if not os.path.isfile(file_path):
            QMessageBox.critical(self, "Invalid File", "The selected item is not a valid file.")
            return
        try:
            df = logic.load_csv(file_path)
            self.parent.df = df
            QMessageBox.information(self, "File Loaded", f"Data loaded successfully from:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Loading Error", f"An error occurred:\n{e}")