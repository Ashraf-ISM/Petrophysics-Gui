import sys
import pandas as pd
import lasio
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QWidget, QPushButton, QLineEdit, QMessageBox, QFileDialog, QLabel, QHeaderView
)
from PyQt5.QtCore import Qt


class LASDataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LAS Data Viewer and Editor")
        self.resize(800, 600)

        self.las_data = None  # Store loaded LAS data as a pandas DataFrame

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Buttons
        self.load_las_button = QPushButton("Load LAS File")
        self.load_txt_button = QPushButton("Load TXT File")
        self.apply_changes_button = QPushButton("Apply Header Changes")
        self.save_button = QPushButton("Save Data")
        
        layout.addWidget(self.load_las_button)
        layout.addWidget(self.load_txt_button)
        layout.addWidget(self.apply_changes_button)
        layout.addWidget(self.save_button)

        # Table for displaying well data
        self.well_data_table = QTableWidget()
        layout.addWidget(self.well_data_table)

        # Signal connections
        self.load_las_button.clicked.connect(self.load_las_data)
        self.load_txt_button.clicked.connect(self.load_txt_data)
        self.apply_changes_button.clicked.connect(self.apply_header_changes)
        self.save_button.clicked.connect(self.save_renamed_data)

    def load_las_data(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open LAS File", "", "LAS Files (*.las);;All Files (*)")
            if not file_path:
                return
            las = lasio.read(file_path)
            self.las_data = las.df().reset_index()
            self.update_well_data_table(self.las_data)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading LAS file: {str(e)}")

    def load_txt_data(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open TXT File", "", "TXT Files (*.txt);;CSV Files (*.csv);;All Files (*)")
            if not file_path:
                return
            self.las_data = pd.read_csv(file_path, delimiter=',')
            self.update_well_data_table(self.las_data)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading TXT file: {str(e)}")

    def update_well_data_table(self, df):
        """Populate the QTableWidget with data from a DataFrame."""
        self.well_data_table.setRowCount(df.shape[0])
        self.well_data_table.setColumnCount(df.shape[1])
        self.well_data_table.setHorizontalHeaderLabels(df.columns)
        
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.well_data_table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        
        # Enable column renaming
        self.well_data_table.horizontalHeader().setSectionsClickable(True)
        self.well_data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def apply_header_changes(self):
        try:
            # Fetch new column names from the table widget
            column_count = self.well_data_table.columnCount()
            new_headers = []
            for col in range(column_count):
                new_headers.append(self.well_data_table.horizontalHeaderItem(col).text())
            
            # Update the DataFrame's column names
            self.las_data.columns = new_headers
            
            QMessageBox.information(self, "Header Changes Applied", "Column headers updated successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error applying header changes: {str(e)}")

    def save_renamed_data(self):
        try:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
            )
            if save_path:
                if save_path.endswith('.csv'):
                    self.las_data.to_csv(save_path, index=False)
                elif save_path.endswith('.xlsx'):
                    self.las_data.to_excel(save_path, index=False)
                else:
                    QMessageBox.warning(self, "Unsupported Format", "File format not supported for saving.")
                    return
                
                QMessageBox.information(self, "Save Successful", f"Data saved successfully to {save_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error saving file: {str(e)}")

    def plot_data(self):
        """Example method to show how data can be used after renaming."""
        try:
            if 'DEPTH' not in self.las_data.columns:
                QMessageBox.warning(self, "Error", "Column 'DEPTH' not found in the dataset.")
                return
            # Proceed with plotting (or any processing)
            depth = self.las_data['DEPTH']
            print(f"DEPTH column: {depth.head()}")
        except KeyError as e:
            QMessageBox.warning(self, "Error", f"KeyError: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = LASDataApp()
    main_window.show()
    sys.exit(app.exec_())
