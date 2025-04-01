from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
import logic

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Reference to MainWindow
        layout = QVBoxLayout()
        
        # Button to load CSV file
        btn_load_csv = QPushButton("Load CSV")
        btn_load_csv.clicked.connect(self.load_csv)
        layout.addWidget(btn_load_csv)
        
        # Button to load JSON file
        btn_load_json = QPushButton("Load JSON")
        btn_load_json.clicked.connect(self.load_json)
        layout.addWidget(btn_load_json)
        
        # Button to save CSV file
        btn_save_csv = QPushButton("Save CSV")
        btn_save_csv.clicked.connect(self.save_csv)
        layout.addWidget(btn_save_csv)
        
        # Button to save JSON file
        btn_save_json = QPushButton("Save JSON")
        btn_save_json.clicked.connect(self.save_json)
        layout.addWidget(btn_save_json)
        
        # Status label to show file operation feedback
        self.status_label = QLabel("No data loaded.")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.parent.df = logic.load_csv(file_path)
                self.status_label.setText(f"Loaded CSV: {file_path}")
            except Exception as e:
                self.status_label.setText(f"Error loading CSV: {e}")
                
    def load_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if file_path:
            try:
                self.parent.df = logic.load_json(file_path)
                self.status_label.setText(f"Loaded JSON: {file_path}")
            except Exception as e:
                self.status_label.setText(f"Error loading JSON: {e}")
                
    def save_csv(self):
        if self.parent.df is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
            if file_path:
                try:
                    logic.save_csv(self.parent.df, file_path)
                    self.status_label.setText(f"CSV saved to: {file_path}")
                except Exception as e:
                    self.status_label.setText(f"Error saving CSV: {e}")
        else:
            self.status_label.setText("No data to save.")
            
    def save_json(self):
        if self.parent.df is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json)")
            if file_path:
                try:
                    logic.save_json(self.parent.df, file_path)
                    self.status_label.setText(f"JSON saved to: {file_path}")
                except Exception as e:
                    self.status_label.setText(f"Error saving JSON: {e}")
        else:
            self.status_label.setText("No data to save.")
