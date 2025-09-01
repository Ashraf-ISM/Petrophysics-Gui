import sys
import dlisio  # Correct import
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Main Application Window
class DLISViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DLIS Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.data = None  # To store loaded DLIS data

        # Create GUI elements
        self.init_ui()

    def init_ui(self):
        # Layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Buttons
        load_button = QPushButton('Load DLIS File', self)
        load_button.clicked.connect(self.load_dlis)
        button_layout.addWidget(load_button)

        plot_button = QPushButton('Plot Data', self)
        plot_button.clicked.connect(self.plot_data)
        button_layout.addWidget(plot_button)

        # Metadata text box
        self.metadata_text = QTextEdit(self)
        self.metadata_text.setReadOnly(True)

        # Matplotlib Canvas for plotting
        self.figure = plt.Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        
        # Add widgets to layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.metadata_text)
        main_layout.addWidget(self.canvas)

        # Set layout for the window
        self.setLayout(main_layout)

    def load_dlis(self):
        # Open file dialog to select the DLIS file
        file_dialog = QFileDialog(self)
        filepath, _ = file_dialog.getOpenFileName(self, 'Open DLIS File', '', 'DLIS Files (*.DLIS);;All Files (*)')

        if filepath:
            try:
                # Use dlisio to load the DLIS file
                dlis_file = dlisio.DLISFile(filepath)
                dlis_file.read()

                self.data = dlis_file
                QMessageBox.information(self, 'Success', f'File loaded successfully: {filepath}')
                self.show_metadata()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to load DLIS file: {e}')

    def show_metadata(self):
        # Clear existing metadata in the text box
        self.metadata_text.clear()

        if self.data:
            metadata = f"File Info: {self.data.describe()}\n\n"
            for frame in self.data.frames:
                metadata += f"Frame Name: {frame.name}\n"
                metadata += f"Index Type: {frame.index_type}\n"
                metadata += f"Depth Interval: {frame.index_min} - {frame.index_max}\n"
                metadata += f"Depth Spacing: {frame.spacing}\n\n"
            self.metadata_text.setPlainText(metadata)
        else:
            self.metadata_text.setPlainText("No data loaded")

    def plot_data(self):
        if not self.data:
            QMessageBox.warning(self, 'Error', 'Please load a DLIS file first.')
            return

        # Extract curves from data
        frame1 = self.data.frames[0]  # Assuming the first frame contains the curves
        dtc = frame1['CHANNEL'].get('PWF4', None)

        if dtc is None:
            QMessageBox.warning(self, 'Error', 'DTCO curve not found in the DLIS file.')
            return

        # Extract depth and other curves
        depth = frame1['TDEP'] * 0.00254  # Convert depth to meters
        dtco = frame1['DTCO']
        dtsm = frame1['DTSM']

        # Create plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(depth, dtco, label="DTCO")
        ax.plot(depth, dtsm, label="DTSM", color='brown')
        ax.set_xlabel('Depth (m)')
        ax.set_ylabel('Velocity (m/s)')
        ax.set_title('DTCO and DTSM vs Depth')
        ax.legend()

        # Refresh the canvas
        self.canvas.draw()

# Run the application
def main():
    app = QApplication(sys.argv)
    viewer = DLISViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
s