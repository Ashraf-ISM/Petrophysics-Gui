import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QTabWidget,
    QFileDialog
)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap 
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QCheckBox,QLabel, QGroupBox, QSlider, QSizePolicy,QGridLayout,QSplashScreen,QListWidget, QTabWidget,QDesktopWidget, QProgressBar, QFormLayout,QColorDialog,QDialog,QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap 
from PyQt5.QtCore import Qt,QTimer
import sys
import lasio
from  dlisio import dlis
import pandas as pd 
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import numpy as np
import seaborn as sns
import plotly.express as px
import logging
logging.basicConfig(level=logging.ERROR)  # Only log errors and above by default
from TripleCombo import TripleComboPlot  # Import your custom plot class
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest









from backend import PetroAnalysis


import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.petro_analysis_widget = PetroAnalysis()
        self.tab_widget.addTab(self.petro_analysis_widget, "PetroAnalysis")

       # self.petrophysics_widget = TripleComboPlot()
#        self.tab_widget.addTab(self.petrophysics_widget, "TripleComboPlots Analysis")

        self.setWindowTitle("PetroAnalysis Main Window")
        self.resize(1200, 800)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        export_csv_action = QAction("Export as CSV", self)
        export_csv_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_csv_action)

        export_png_action = QAction("Export Plot as PNG", self)
        export_png_action.triggered.connect(lambda: self.export_plot('png'))
        file_menu.addAction(export_png_action)

        export_pdf_action = QAction("Export Plot as PDF", self)
        export_pdf_action.triggered.connect(lambda: self.export_plot('pdf'))
        file_menu.addAction(export_pdf_action)

       
        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        # About Us Menu
        about_us_menu = menu_bar.addMenu("&About Us")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        about_us_menu.addAction(about_action)

        motive_action = QAction("Motive", self)
        motive_action.triggered.connect(self.show_motive)
        about_us_menu.addAction(motive_action)

    def export_csv(self):
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, 'las_data') and not current_widget.las_data.empty:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Results as CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

            if file_path:
                try:
                    current_widget.las_data.to_csv(file_path, index=False)
                    QMessageBox.information(self, "Success", "Results exported successfully as CSV!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to export CSV: {e}")
        else:
            QMessageBox.warning(self, "No Data", "No data available to export.")

    def export_plot(self, format='png'):
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, 'evaluation_canvas'):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, f"Export Plot as {format.upper()}", "", f"{format.upper()} Files (*.{format});;All Files (*)", options=options)

            if file_path:
                try:
                    logging.debug("Rendering the plot before saving.")
                    current_widget.evaluation_canvas.figure.canvas.draw()
                    current_widget.evaluation_canvas.figure.savefig(file_path, format=format)
                    QMessageBox.information(self, "Success", f"Plot exported successfully as {format.upper()}!")
                except Exception as e:
                    logging.error(f"Error during plot export: {e}")
                    QMessageBox.critical(self, "Error", f"Failed to export plot: {e}")
        else:
            QMessageBox.warning(self, "No Plot", "No plot available to export.")


    def show_help(self):
        QMessageBox.information(self, "Help",
        """<html>
        <h1>Help - DARKSPY</h1>
        <p>Welcome to the DARKSPY Help Section!</p>
        <p>This application is designed to facilitate the analysis and visualization of well log data.</p>
        <h2>Getting Started:</h2>
        <ol>
            <li>Launch the application.</li>
            <li>Import your data files by navigating to the 'File' menu and selecting 'Open'.</li>
            <li>Once the data is loaded, you can view various analyses and visualizations from the main menu.</li>
        </ol>
        <h2>Key Features:</h2>
        <ul>
            <li>Data Loading: Import well data from LAS, CSV, and DLIS formats.</li>
            <li>Statistical Analysis: Perform descriptive statistics to analyze geological data.</li>
            <li>Visualizations: Create plots to visualize data trends and relationships.</li>
            <li>User Interface: Navigate easily with a simple and intuitive layout.</li>
        </ul>
        <h2>Common Tasks:</h2>
        <ol>
            <li>Loading Data: Click on 'File' > 'Open' and select your data file.</li>
            <li>Viewing Data: Once loaded, your data will be displayed in the main window. Use the tabs to navigate between different analyses.</li>
            <li>Exporting Results: To save your analysis, click 'File' > 'Save As' to export your results.</li>
        </ol>
        <h2>Troubleshooting:</h2>
        <ul>
            <li><b>Issue:</b> Data not loading: Ensure your file format is supported (LAS, CSV, DLIS).</li>
            <li><b>Issue:</b> Application crashes: Try restarting the application or checking your data for errors.</li>
        </ul>
        <p>For further assistance, please contact:</p>
        <p>Md Ashraf<br>Email: <a href="mailto:mdashraf6209@gmail.com">mdashraf6209@gmail.com</a></p>
        <p>We appreciate your feedback and are here to help!</p>
        </html>""")

    def show_about(self):
        QMessageBox.information(self,
                                "About DARKSPY",
                                """<html>
                                <h1>About DARKSPY</h1>
                                <p>DARKSPY is a simple application for Petrophysical analysis and visualization.</p>
                                <p>It is developed using Python and PyQt5.</p>
                                </html>""")



    from PyQt5.QtWidgets import QMessageBox

    def show_motive(self):
        QMessageBox.information(
            self,
            "Motive",
            """<html>
            <head>
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        color: #333;
                        background-color: #f9f9f9;
                        padding: 10px;
                    }
                    h1 {
                        color: #0056b3;
                        text-align: center;
                        font-size: 24px;
                        margin-bottom: 20px;
                    }
                    p {
                        font-size: 14px;
                        line-height: 1.6;
                        margin: 10px 0;
                    }
                    .highlight {
                        color: #0073e6;
                        font-weight: bold;
                    }
                    a {
                        color: #0073e6;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    .footer {
                        margin-top: 20px;
                        font-size: 12px;
                        text-align: center;
                        color: #555;
                    }
                </style>
            </head>
            <body>
                <h1>Motive</h1>
                <p>
                    The motive behind the development of <span class="highlight">DARKSPY</span> is to create an educational graphical 
                    user interface (GUI) that enhances the processing and interpretation of well-log data.
                </p>
                <p>
                    This project is part of an initiative to deliver an application tailored to the needs of geoscientists 
                    and engineers engaged in petrophysical analysis.
                </p>
                <p>
                    By providing a smooth workflow and robust analytical tools, <span class="highlight">DARKSPY</span> aims to empower 
                    users to explore and interpret geological data interactively. It aspires to be a valuable resource for 
                    both students and professionals, fostering deeper insights into subsurface properties.
                </p>
                <p>
                    This effort is spearheaded by a dedicated team under the guidance of:
                </p>
                <p class="footer">
                    <b>Instructor:</b> Partha Pratim Mandal<br>
                    Assistant Professor, IIT(ISM) Dhanbad<br>
                    <a href="mailto:partham@iitism.ac.in">partham@iitism.ac.in</a>
                </p>
            </body>
            </html>"""
        )



#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    window = MainWindow()
#    window.show()
#    sys.exit(app.exec_())
#    
    
    
def main():
    app = QApplication(sys.argv)
    
    # Splash Screen Setup
    splash_pix = QPixmap("app.webp")  # Replace with the path to your splash image
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.FramelessWindowHint)  # Frameless look for the splash
    splash.show()
    
    # Simulate a loading delay
    QTimer.singleShot(3000, splash.close)  # Show the splash for 3 seconds
    
    # Create the main window
    main_window = MainWindow()
    QTimer.singleShot(3000, main_window.show)  # Show the main window after the splash

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

