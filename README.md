# Minimalistic Data Analytics App

**Module Code:** IY499 – Introduction to Programming  
**Author:** Imronbek  
**Teacher:** Marzieh Farahani  
**Due Date:** Thursday 10th April 2025, 12 noon

---

## 1. Overview

The Minimalistic Data Analytics App is a desktop application built with Python using PySide6. This application allows users to load data from CSV (or JSON) files, compute descriptive and grouped statistics, generate interactive graphs, and view data in an Excel-like table. Inspired by Apple’s design aesthetics and a retro “Fallout” terminal theme, the application features a black background with bright green text and a clean, minimalistic layout.

---

## 2. Features

- **Multi-Page Interface:**  
  The application includes four main pages:
  - **Home Page:** Scans a default folder for CSV files, allows folder browsing, and loads selected files.
  - **Statistics Page:** Displays descriptive statistics and enables grouped analysis.
  - **Graphs Page:** Dynamically generates various graphs (Bar, Line, Scatter, Histogram, Pie) using Qt Charts.
  - **Table Page:** Presents the loaded dataset in a sortable, spreadsheet-like table.
  
- **Robust Data Processing:**  
  The backend (logic module) handles data I/O, normalization (e.g., cleaning column names), and statistical computations.

- **Dynamic Graph Generation:**  
  Depending on the selected graph type, the input axis controls adjust dynamically (one-axis graphs versus two-axis graphs).

- **Fallout Theme:**  
  The entire application uses a dark theme—black backgrounds with bright green text—for a retro terminal look.

---

## 3. Project Structure

The project is organized into the following modules and folders:

- **app.py:**  
  Contains the MainWindow class, which manages shared data and page navigation (using QStackedWidget). It includes a top toolbar to navigate between Home, Statistics, Graphs, and Table pages.

- **pages/home_page.py:**  
  Implements the HomePage, which automatically scans a specified folder for CSV files, displays the file list, and loads the selected file into a shared Pandas DataFrame.

- **pages/stats_page.py:**  
  Implements the Statistics Page, which shows descriptive statistics computed via Pandas and allows grouping/aggregation of data. The results are displayed both in a text summary and a QTableWidget.

- **pages/graphs_page.py:**  
  Implements the Graphs Page, where users select a graph type (e.g., Bar, Histogram, Pie, Line, Scatter). The controls dynamically update based on the graph type, and graphs are rendered with PySide6’s Qt Charts.

- **pages/table_page.py:**  
  Implements the Table Page, displaying the loaded dataset in a sortable, interactive table view.

- **logic.py:**  
  Contains functions for file I/O (CSV/JSON loading and saving), data normalization, statistical calculations, pivot table creation, and helper functions used in graph preparation.

---

## 4. Installation

### Prerequisites

- **Python 3.11** (or higher recommended)  
- **Pip** package manager

### Required Libraries

The application depends on the following Python packages:
- **PySide6**
- **Pandas**
- **NumPy**
- **SciPy**

Install these by running:

```bash
pip install PySide6 pandas numpy scipy
