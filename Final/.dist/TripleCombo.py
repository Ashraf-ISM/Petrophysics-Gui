import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QGridLayout, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy as np
import plotly.graph_objects as go
from PyQt5.QtWebEngineWidgets import QWebEngineView
import lasio
import matplotlib.pyplot as plt

class TripleComboPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triple Combo Plot Tool")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        self.layout = QVBoxLayout(self)

        # **Button Section at the Top**
        button_layout = QHBoxLayout()

        # ListWidget for Gamma Ray (GR)
        self.gr_list_widget = QListWidget()
        self.gr_list_widget.setToolTip("Select Gamma Ray (GR) options.")
        self.gr_list_widget.setSelectionMode(QListWidget.MultiSelection)  # Enable multi-selection
        self.gr_list_widget.setFixedSize(150,70)  # Set fixed width for GR list widget

        # ListWidget for Resistivity
        self.resistivity_list_widget = QListWidget()
        self.resistivity_list_widget.setToolTip("Select Resistivity options.")
        self.resistivity_list_widget.setSelectionMode(QListWidget.MultiSelection)  # Enable multi-selection
        self.resistivity_list_widget.setFixedSize(150,70)  # Set fixed width for Resistivity list widget

        # ListWidget for Porosity
        self.porosity_list_widget = QListWidget()
        self.porosity_list_widget.setToolTip("Select Porosity options.")
        self.porosity_list_widget.setSelectionMode(QListWidget.MultiSelection)  # Enable multi-selection
        self.porosity_list_widget.setFixedSize(150,70)  # Set fixed width for Porosity list widget

        # Adding list widgets and labels to the button layout
        button_layout.addWidget(QLabel("Gamma Ray (GR):"))
        button_layout.addWidget(self.gr_list_widget)

        button_layout.addWidget(QLabel("Resistivity:"))
        button_layout.addWidget(self.resistivity_list_widget)

        button_layout.addWidget(QLabel("Porosity:"))
        button_layout.addWidget(self.porosity_list_widget)

        # **File Upload Section**
        self.upload_button = QPushButton("Upload Data")
        self.upload_button.clicked.connect(self.upload_data)
        button_layout.addWidget(self.upload_button)

        # Plot button
        self.plot_button = QPushButton("Plot")
        button_layout.addWidget(self.plot_button)
        self.plot_button.clicked.connect(self.plot_triple_combo)

        # Add button layout to main layout
        self.layout.addLayout(button_layout)

        # **Plot Display Section**
        self.plot_view = QWebEngineView()
        self.layout.addWidget(self.plot_view, stretch=1)


        self.las_data = None  # To store LAS file data

    def upload_data(self):
        # Open file dialog to select the LAS file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open LAS File", "", "LAS Files (*.las);;All Files (*)", options=options)

        if file_path:
            # Read the LAS file
            self.las_data = lasio.read(file_path)

            # Populate the list widgets with the columns from the LAS file
            columns = list(self.las_data.keys())
            self.gr_list_widget.clear()
            self.resistivity_list_widget.clear()
            self.porosity_list_widget.clear()

            # Populate each list widget with all available curves (columns)
            self.gr_list_widget.addItems(columns)
            self.resistivity_list_widget.addItems(columns)
            self.porosity_list_widget.addItems(columns)

    def plot_triple_combo(self):
        # Check if the LAS data has been loaded
        if self.las_data is None:
            print("Error: No data uploaded.")
            return
        
        # Retrieve selected options from list widgets
        gr_items = self.gr_list_widget.selectedItems()
        gr_options = [item.text() for item in gr_items]

        resistivity_items = self.resistivity_list_widget.selectedItems()
        resistivity_options = [item.text() for item in resistivity_items]

        porosity_items = self.porosity_list_widget.selectedItems()
        porosity_options = [item.text() for item in porosity_items]

        # Extract necessary curves from the LAS data
        try:
            
            # Check for 'DEPTH' or 'DEPT' column and assign accordingly
            if 'DEPTH' in self.las_data.keys():
                well = {"DEPTH": self.las_data["DEPTH"]}
            elif 'DEPT' in self.las_data.keys():
                well = {"DEPTH": self.las_data["DEPT"]}
            else:
                raise KeyError("Neither 'DEPTH' nor 'DEPT' columns found in the LAS file.")
            
            # Add selected GR curves to the well dictionary
            for option in gr_options:
                if option in self.las_data.keys():
                    well[option] = self.las_data[option]  # Use selected GR curves
                else:
                    print(f"Warning: {option} curve not found in the LAS file.")
            
            # Add selected Resistivity curves to the well dictionary
            for option in resistivity_options:
                if option in self.las_data.keys():
                    well[option] = self.las_data[option]  # Use selected Resistivity curves
                else:
                    print(f"Warning: {option} curve not found in the LAS file.")
            
            # Add selected Porosity curves to the well dictionary
            for option in porosity_options:
                if option in self.las_data.keys():
                    well[option] = self.las_data[option]  # Use selected Porosity curves
                else:
                    print(f"Warning: {option} curve not found in the LAS file.")
        
        except KeyError as e:
            print(f"Error: Missing curve {e} in the LAS file.")
            return
        
        #
        ## Initialize the plot
        #fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 12))
#
        ## Gamma Ray track - Plot all selected Gamma Ray columns on the same plot
        #for gr_curve in gr_options:
        #    ax1.plot(well[gr_curve], well["DEPTH"], label=gr_curve)
        #
        #ax1.set_xlabel("Gamma Ray")
        #ax1.xaxis.label.set_color("green")
        #ax1.set_xlim(0, 200)
        #ax1.set_ylabel("Depth (m)")
        #ax1.tick_params(axis='x', colors="green")
        #ax1.spines["top"].set_edgecolor("green")
        #ax1.title.set_color('green')
        #ax1.set_xticks([0, 50, 100, 150, 200])
        #ax1.legend()
        # Initialize the plot
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(6, 8))
        
        # Gamma Ray and Caliper track - Plot on the same graph
        # Gamma Ray plot
        for gr_curve in gr_options:
            if gr_curve != "CALI":
                ax1.plot(well[gr_curve], well["DEPTH"], label=f"Gamma Ray: {gr_curve}", color="green")
        
        # Configure primary x-axis for Gamma Ray
        ax1.xaxis.label.set_color("green")
        ax1.set_xlim(0, 200)
        ax1.set_ylabel("Depth (m)")
        ax1.set_xlabel("Gamma Ray")
        ax1.tick_params(axis='x', colors="green")
        ax1.spines["top"].set_edgecolor("green")
        ax1.spines['top'].set_position(('axes',1.01))
        ax1.legend()
        ax1.title.set_color("green")
        ax1.set_xticks([0, 50, 100, 150, 200])
        
        # Secondary x-axis for Caliper
        ax1_twin = ax1.twiny()
        
        # Caliper plot using the same dictionary
        if "CALI" in well:  # Ensure the Caliper curve exists
            ax1_twin.plot(well["CALI"], well["DEPTH"], label="Caliper", color="blue", linestyle="--")
        
        # Configure secondary x-axis for Caliper
        ax1_twin.set_xlabel("Caliper")
        ax1_twin.xaxis.label.set_color("blue")
        ax1_twin.set_xlim(0, 14)
        ax1_twin.tick_params(axis='x', colors="blue")
        ax1_twin.spines["top"].set_edgecolor("blue")
        ax1_twin.spines['top'].set_position(('axes',1.05))
        ax1_twin.spines['top'].set_visible(True)
        ax1_twin.legend()
        # Set depth range for both axes
        ax1.set_ylim(well["DEPTH"].max(), well["DEPTH"].min())  # Depth should decrease downward
        ax1_twin.set_ylim(well["DEPTH"].max(), well["DEPTH"].min())
        
        # Add legends
        ax1.legend(loc="upper left")
        ax1_twin.legend(loc="upper right")
        
        # Continue with Resistivity and Porosity tracks


       # Resistivity track - Plot all selected resistivity columns on the same plot
        for resistivity_curve in resistivity_options:
            ax2.plot(well[resistivity_curve], well["DEPTH"], label=resistivity_curve,linewidth=0.8)
        
        ax2.set_xlabel("Resistivity")
        ax2.set_xlim(0.1, 10000)  # Set a reasonable range for log scale (logarithmic scale cannot include 0)
        ax2.set_xscale("log")     # Set the x-axis to a logarithmic scale
        ax2.set_ylabel("Depth (m)")
        ax2.legend()
        ax2.tick_params(axis='x', colors="red")
        ax2.spines["top"].set_edgecolor("red")
        ax2.set_xticks([0.1, 1, 10, 100, 1000, 10000])  # Specify tick positions
        ax2.get_xaxis().set_major_formatter(plt.ScalarFormatter())  # Use scalar format for log axis

        
        # Porosity track - Plot all selected porosity columns on the same plot
        for porosity_curve in porosity_options:
            ax3.plot(well[porosity_curve], well["DEPTH"], label=porosity_curve)
        
        ax3.set_xlabel("Porosity")
        ax3.set_xlim(-0.45, 0.8)
        ax3.xaxis.label.set_color("purple")
        ax3.tick_params(axis='x', colors="purple")
        ax3.spines["top"].set_edgecolor("purple")
        ax3.legend()

        # Common functions for setting up the plot can be extracted into
        # a loop to avoid repeating code
        for ax in [ax1, ax2, ax3]:
            ax.set_ylim(max(well["DEPTH"]), min(well["DEPTH"]))  # Depth increases downwards
            ax.grid(which='major', color='lightgrey', linestyle='-')
            ax.xaxis.set_ticks_position("top")
            ax.xaxis.set_label_position("top")
            ax.spines["top"].set_position(("axes", 1.0))
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TripleComboPlot()
    window.show()
    sys.exit(app.exec_())
