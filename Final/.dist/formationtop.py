from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QLineEdit, QGroupBox, QFileDialog, QMessageBox
import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt,QTimer


class FormationTopTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main Layout
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Formation Top Identification")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # File Loading Section
        self.file_load_btn = QPushButton("Load Well Log Data")
        self.file_load_btn.clicked.connect(self.load_well_log_data)
        layout.addWidget(self.file_load_btn)

        # Dropdowns for Curve Selection
        curve_layout = QHBoxLayout()
        self.curve_label = QLabel("Select Curve:")
        self.curve_dropdown = QComboBox()
        curve_layout.addWidget(self.curve_label)
        curve_layout.addWidget(self.curve_dropdown)
        layout.addLayout(curve_layout)

        # Threshold Inputs for Formation Detection
        threshold_layout = QHBoxLayout()
        self.threshold_label = QLabel("Set Threshold Value:")
        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText("Enter threshold value")
        threshold_layout.addWidget(self.threshold_label)
        threshold_layout.addWidget(self.threshold_input)
        layout.addLayout(threshold_layout)

        # Action Buttons
        button_layout = QHBoxLayout()
        self.detect_btn = QPushButton("Detect Formation Tops")
        self.detect_btn.clicked.connect(self.detect_formation_tops)
        self.clear_btn = QPushButton("Clear Results")
        self.clear_btn.clicked.connect(self.clear_results)
        button_layout.addWidget(self.detect_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Top Depth", "Bottom Depth"])
        layout.addWidget(self.results_table)

        self.setLayout(layout)

        # Data Storage
        self.data = None

    def load_well_log_data(self):
        """Load well log data from a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Well Log File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.curve_dropdown.clear()
                self.curve_dropdown.addItems(self.data.columns)
                QMessageBox.information(self, "Success", "Data loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load data: {e}")

    def detect_formation_tops(self):
        """Detect formation tops based on selected curve and threshold."""
        if self.data is None:
            QMessageBox.warning(self, "Warning", "Please load well log data first.")
            return

        selected_curve = self.curve_dropdown.currentText()
        try:
            threshold = float(self.threshold_input.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid threshold value.")
            return

        if selected_curve not in self.data.columns:
            QMessageBox.warning(self, "Warning", "Selected curve not found in the dataset.")
            return

        curve_data = self.data[selected_curve]
        depth_column = self.data.columns[0]

        tops = []
        in_formation = False
        start_depth = None

        for depth, value in zip(self.data[depth_column], curve_data):
            if value >= threshold and not in_formation:
                in_formation = True
                start_depth = depth
            elif value < threshold and in_formation:
                in_formation = False
                tops.append((start_depth, depth))

        # Populate results table
        self.results_table.setRowCount(len(tops))
        for i, (top, bottom) in enumerate(tops):
            self.results_table.setItem(i, 0, QTableWidgetItem(f"{top:.2f}"))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{bottom:.2f}"))

        QMessageBox.information(self, "Detection Complete", f"Found {len(tops)} formation tops.")

    def clear_results(self):
        """Clear results table."""
        self.results_table.setRowCount(0)

