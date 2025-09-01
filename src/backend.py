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
from TripleCombo import TripleComboPlot  # Import your custom plot class
from mpl_toolkits.mplot3d import Axes3D
import missingno as msno




#####################################3



from PyQt5.QtWidgets import QVBoxLayout,QWidget ,QTableWidget,QComboBox,QTableWidgetItem,QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore , QtGui ,QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import pandas as pd 
from typing import List

class MplCanvas(FigureCanvas):
    def __init__(self,fig,parent=None,):
        super(MplCanvas, self).__init__(fig)


class MplWidgetMltrk(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.var_names = []
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas)
        self.vlayout.addWidget(self.toolbar)
        self.setLayout(self.vlayout)
        self.data = None
        
    
    def set_dataframe(self,data : pd.DataFrame ,color_map : str = 'tab10'):
        self.figure.clear()
        self.data = data
        self.columns = list(self.data.columns)
        self.depth_col = self.columns[0]

        self.depthmax = np.max(self.data[self.depth_col].values)
        self.depthmin = np.min(self.data[self.depth_col].values)
        self.cmap = plt.cm.get_cmap(color_map ,len(self.columns))
        plot_colors = {}
        for i in range(len(self.columns)):
            plot_colors[self.columns[i]] = self.cmap(i)
        self.plot_colors =plot_colors
    
    def perform_plotting(self,plotting_curve : List[str] , curve_for_semilog : List[str] = None):
        if self.data is not None:
            self.figure.clear()
            n_vars = len(plotting_curve)
            if n_vars:
                ax = self.figure.add_subplot(1, n_vars, 1)  
                for i, var_name in enumerate(plotting_curve):
                    if i > 0:
                        ax = self.figure.add_subplot(1, n_vars, i + 1, sharey=ax)
                    color = self.plot_colors[var_name]
                    ax.plot(self.data[var_name],self.data[self.depth_col],color = color)
                    ax.xaxis.set_label_position('top')
                    xlabel_ax = var_name
                    ax.set_xlabel(xlabel_ax,color=color)
                    ax.tick_params(axis='x', colors=color)
                    ax.spines['top'].set_edgecolor(color)
                    ax.set_ylim(self.depthmax,self.depthmin)
                    ax.grid(visible=True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
                    # if i != 0 :
                    #     ax.set_yticklabels([])
                    #     ax.set_ylabel('')
                    #     ax.set_yticks([])
                    if i == 0:
                        ax.set_ylabel('Depth')
                                            
                    if curve_for_semilog:
                        if var_name in curve_for_semilog:
                            try:
                                ax.set_xscale('log')
                            except Exception as e:
                                print(f"Error in semilogx for {var_name} : {e}")
                self.figure.tight_layout()
                self.canvas.draw()
from PyQt5 import QtWidgets ,  QtGui , QtCore
import typing 
from typing import List, Tuple, Dict, Any , Callable
import pandas as pd
from PyQt5 import QtWidgets ,  QtGui , QtCore
import typing 
from typing import List, Tuple, Dict, Any , Callable
import pandas as pd
from DataVisualizer import Ui_visualizerForm


resistivity_mnemonics = ['RT','RT10','RT20','RT50','RT30','RT60','RT20','RT50','RT60']+['AT10','AT20','AT30','AT50','AT60','AT20','AT50','AT60']+['AF10','AF20','AF30','AF50','AF60','AF20','AF50','AF60']+['AO10','AO20','AO30','AO50','AO60','AO20','AO50','AO60'] + ['RESD','RESS','RESM']
class VisulizationPage(QtWidgets.QWidget,Ui_visualizerForm):
    def __init__(self, parent=None):
        super(VisulizationPage, self).__init__(parent)
        self.setupUi(self)
        self.scrollArea : QtWidgets.QScrollArea
        self.multitrackwidget = MplWidgetMltrk(self)
        self.scrollArea.setWidget(self.multitrackwidget)
            
    def set_dataframe_to_visualize(self,df : pd.DataFrame):
        self.df = df
        self.comboBox: QtWidgets.QComboBox
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox.addItems(df.columns)
        self.comboBox_2.addItems(df.columns)
        self.multitrackwidget.set_dataframe(df)
        
        res_col= [col for col in df.columns if col in resistivity_mnemonics]
        
        if res_col:
            self.comboBox_2.setItemsSelected(res_col)
        self.pushButton : QtWidgets.QPushButton
        self.pushButton.clicked.connect(self.plotting_button_clicked)
            
    def plotting_button_clicked(self):
        curve_for_plotting = self.comboBox.getSelectedItems()
        curve_for_semilog = self.comboBox_2.getSelectedItems()
        self.multitrackwidget.perform_plotting(curve_for_plotting , curve_for_semilog)
        
        
    
        

######################################






class PetroAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PetroAnalysis')
        self.resize(900, 800)
        screen=QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - self.width()) / 2), int((screen.height() - self.height()) / 2))
        

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.header_text=None

        #######Task menu############
        ################Demo file use##########
       # self.demo_file_path = os.path.join(os.getcwd(), "demo_file.las")
        
        ############################################
        
        # Add title for the app name "Petro"
        # title_label = QLabel("DARKSPY")
        # title_label.setFont(QFont('Times New Roman', 20, QFont.Bold))
        # title_label.setAlignment(Qt.AlignCenter)
        # title_label.setStyleSheet(
        #     "background-color: white; "
        #     "border: 2px solid black; "
        #     "padding: 10px; "
        #     "border-radius: 5px;"
        # )
       # main_layout.addWidget(title_label)
        
        ######################

        # Tabs for Data Loading and Basic Visualization
        tab_widget = QTabWidget()        
        tab_widget.addTab(self.create_data_loading_tab(), QIcon('data-loading.png'), "Data Loading ")
        tab_widget.addTab(self.create_data_loading2_tab(), QIcon('app.webp'), "Well Data and Stats")
        tab_widget.addTab(self.create_visualization_tab(), QIcon('plot.jpeg'), "Basic Visualization")
        tab_widget.addTab(self.create_formation_evaluation_tab(), QIcon('app.webp'), "Formation Evaluation")
        #tab_widget.addTab(self.create_formation_top_tab(), QIcon('app.webp'), "Formation Top Identification")
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        # Set custom styling for the app
        self.setStyle()
        #################### Color for different sections####################
    def setStyle(self):
        
        # Set the palette for custom colors
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f0f0"))  # Light grey background
        palette.setColor(QPalette.WindowText, QColor("#333333"))  # Dark grey text
        palette.setColor(QPalette.Button, QColor("#007BFF"))  # Blue buttons
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))  # White text on buttons
        palette.setColor(QPalette.Highlight, QColor("#0056b3"))  # Darker blue for selected items
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))  # White text on selected items
        palette.setColor(QPalette.Base, QColor("#FFFFFF"))  # White background for text input
        palette.setColor(QPalette.AlternateBase, QColor("#f0f0f0"))  # Light grey for alternate rows
        palette.setColor(QPalette.ToolTipBase, QColor("#FFFFFF"))  # White background for tooltips
        palette.setColor(QPalette.ToolTipText, QColor("#333333"))  # Dark grey text for tooltips
        self.setPalette(palette)
        # Set the font for the application
        font = QFont("Arial", 14)
        self.setFont(font)
        # Set the stylesheet for additional styling
        # Set the stylesheet for additional styling
        self.setStyleSheet("QPushButton {background-color: #007BFF; color: white; border: none; border-radius: 5px; padding: 10px; font-size: 12px;} QPushButton:hover {background-color: #0056b3;} QPushButton:pressed {background-color: #003f7f;} QToolTip {background-color: #FFFFFF; color: #333333; border: 1px solid #CCCCCC; padding: 5px; border-radius: 3px;}")
        ######################################
        ########################################
    def browse_files(self):
        # Functionality for file browsing
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*.csv *.las *.txt *.dlis);;CSV Files (*.csv);;LAS Files (*.las);;Text Files (*.txt);;DLIS Files (*.dlis)",
            options=options,
        )
        if file_name:
            self.las_file_input.setText(file_name)
            if file_name.endswith('.las'):
                self.load_las_data(file_name)
            elif file_name.endswith('.csv'):
                self.load_csv_data(file_name)
            elif file_name.endswith(".txt"):
                self.load_txt_data(file_name)
            elif file_name.endswith(".dlis"):
                self.load_dlis_data(file_name)
                
            self.add_las_data_in_visulization()
            self.add_las_data_in_formation_evaluation()
                
    #########Logic for the dlis data file#######
    def load_dlis_data(self, file_path):
        pass
#################################   
    def load_csv_data(self, file_path):
        try:
            self.las_data=pd.read_csv(file_path,index_col=False)
            #self.las_data.reset_index(inplace=True)
            #self.las_data=self.las_data.drop(self.las_data.columns[0])
            self.las_data.drop(self.las_data.columns[0], axis=1, inplace=True)

            self.update_well_data_table(self.las_data)
            self.update_statistics_table(self.las_data)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading CSV file: {str(e)}")
################LAS DATA############
    def load_las_data(self, file_path):
        try:
            las=lasio.read(file_path)
        # Convert the LAS file data to a pandas DataFrame
            self.las_data = las.df()
            self.las_data = self.las_data.reset_index()  # Reset index if needed
        
        # Update the tables with the data
            self.update_well_data_table(self.las_data)
            self.update_statistics_table(self.las_data)
            self.update_las_header(las)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading LAS file: {str(e)}")
            
            
    def load_txt_data(self, file_path):
        try:
            self.las_data=pd.read_csv(file_path,delimiter=',')
            self.update_well_data_table(self.las_data)
            self.update_statistics_table(self.las_data)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading TXT file: {str(e)}")
#########      # ##########################     
    def update_las_header(self, las):
        try:
            header_lines = []
        # Add Title
            header_lines.append("=== LAS File Header Information ===")
            header_lines.append("")

        # Version Information
            header_lines.append("### Version Information ###")
            for item in las.version:
                header_lines.append(f"{item.mnemonic:<10} : {item.value:<25} ({item.descr})")
            header_lines.append("")

        # Well Information
            header_lines.append("### Well Information ###")
            header_lines.append(f"{'MNEM.':<20}{'UNIT':<20}{'Data Type':<50}{'Information':<70}")
            header_lines.append(f"{'-' * 20}{'-' * 20}{'-' * 20}{'-' * 20}")
            for item in las.well:
                header_lines.append(f"{item.mnemonic:<20}{item.unit:<20}{item.value:<70} {item.descr}")
            header_lines.append("")

        # Parameter Information
            header_lines.append("### Parameter Information ###")
            header_lines.append(f"{'MNEM.':<10}{'UNIT':<15}{'Value':<20}{'Description':<30}")
            header_lines.append(f"{'-' * 10}{'-' * 15}{'-' * 20}{'-' * 30}")
            for item in las.params:
                header_lines.append(f"{item.mnemonic:<10}{item.unit:<15}{item.value:<20} {item.descr}")
            header_lines.append("")

        # Curve Information
            header_lines.append("### Curve Information ###")
            header_lines.append(f"{'MNEM.':<10}{'UNIT':<10}{'Curve':<10}{'Description':<40}")
            header_lines.append(f"{'-' * 10}{'-' * 20 } {'-' * 10}{'-' * 40}")
            for item in las.curves:
            # Check and extract attributes
                #api_code = getattr(item, 'api_code', 'N/A')  # Fallback to 'N/A' if not found
                curve = getattr(item, 'curve', 'N/A')  # Fallback to 'N/A' if not found
                description = getattr(item, 'descr', 'N/A')  # Fallback to 'N/A' if not found
            
                header_lines.append(f"{item.mnemonic:<10}{item.unit:<10}{curve:<10} {description}")
        
            header_lines.append("")

        # Other Information
            header_lines.append("### Additional Information ###")
            other_info = las.other if las.other else "No additional information available."
            header_lines.append(other_info)
        # Join the lines and set to the header text widget
            self.header_text.setText("\n".join(header_lines))
        except AttributeError as e:
            self.header_text.setText(f"Missing attribute: {str(e)}")
        except Exception as e:
            self.header_text.setText(f"Error formatting LAS header: {str(e)}")

        
        ##########################
    def update_well_data_table(self, df):
        # Update the table with well data
        self.well_data_table.setRowCount(df.shape[0])
        self.well_data_table.setColumnCount(df.shape[1])
        self.well_data_table.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.well_data_table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
                
        self.well_data_df=df
                
        
    def update_statistics_table(self, df):
        # Update the statistics table with data statistics
        stats = df.describe(percentiles=[0.05, .25,.5,.75,.95]).T.round(2)
        self.statistics_table.setRowCount(stats.shape[0])
        self.statistics_table.setColumnCount(stats.shape[1])
        self.statistics_table.setHorizontalHeaderLabels(stats.columns)
        self.statistics_table.setVerticalHeaderLabels(stats.index)
        for i in range(stats.shape[0]):
            for j in range(stats.shape[1]):
                self.statistics_table.setItem(i, j, QTableWidgetItem(str(stats.iloc[i, j])))
        self.statistics_df = stats
        
#------------------------------------------------------#

#         SAVE THE DATA AND STATS

#--------------------------------------------------------#










####################----------------------------------------_____########
        
    def create_group_box(self, title, color):
        # Create a styled group box for sections
        group_box = QGroupBox(title)
        group_box.setStyleSheet(f"QGroupBox {{ background-color: {color}; border: 1px solid #000; border-radius: 5px; padding: 10px; font-size: 14px; font-weight: bold; }}")
        return group_box
        ################################################
        ###########Use file for demo###################
        
        
        ######################################################
    def create_data_loading_tab(self):
        # Create Data Loading Tab Layout
        data_loading_tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # LAS File Upload section
        las_group = self.create_group_box("Upload LAS/CSV File", "#D6EAF8")
        las_layout = QVBoxLayout()
        las_upload_layout = QHBoxLayout()
        self.las_file_input = QLineEdit()
        self.las_file_input.setPlaceholderText("Drag and drop file here or browse...")
        browse_button = QPushButton("Browse files")
        browse_button.clicked.connect(self.browse_files)
        las_upload_layout.addWidget(self.las_file_input)
        las_upload_layout.addWidget(browse_button)
        las_layout.addLayout(las_upload_layout)
        #self.use_demo_checkbox = QCheckBox("Use demo file")
        #las_layout.addWidget(self.use_demo_checkbox)
        las_group.setLayout(las_layout)
        
    
    
    ###############################################################
        # Formation Tops and Core Data section
        formation_core_group = self.create_group_box("Formation Tops & Core Data", "#E8F8F5")
        formation_core_layout = QHBoxLayout()
        formation_combo = QComboBox()
        formation_combo.addItems(["Upload Formation Tops"])
        formation_core_layout.addWidget(formation_combo)

        core_combo = QComboBox()
        core_combo.addItems(["Upload Core Data"])
        formation_core_layout.addWidget(core_combo)
        formation_core_group.setLayout(formation_core_layout)









#-----------------------------------__###################
        # LAS File Header Information
        header_info_group = self.create_group_box("LAS File Header Information", "#FDEDEC")
        header_layout = QVBoxLayout()
        self.header_text = QTextEdit()
        self.header_text.setReadOnly(True)
        self.header_text.setPlaceholderText("LAS file header information will appear here after loading.")
        header_layout.addWidget(self.header_text)
        header_info_group.setLayout(header_layout)
###########Header information for the las file################
    
        ###############tabular form for well header info#######
        
        
        ############### 

        # Well Log Unit Conversion
        unit_conversion_group = self.create_group_box("Well Log Unit Conversion", "#FDEDEC")
        unit_conversion_layout = QHBoxLayout()
        unit_conversion_layout.addWidget(QPushButton("Unit Conversion"))
        unit_conversion_group.setLayout(unit_conversion_layout)
        
        
        #Logic for the unit conversion
        
        

        

        # Add groups to layout
        layout.addWidget(las_group)
        layout.addWidget(formation_core_group)
        layout.addWidget(header_info_group)
        layout.addWidget(unit_conversion_group)
        data_loading_tab.setLayout(layout)
        return data_loading_tab
    
    
    
    ##################################33##############
    
    ##########################################################
    ####Data loading 2 tab################
    
        
    def create_data_loading2_tab(self):
        data_loading2_tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

    # Title for Well Data and Stats
        title_label = QLabel("Well Data and Stats")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
 
    # Well Data Table Group
        well_data_group = self.create_group_box("Well Data", "#FCF3CF")
        well_data_layout = QHBoxLayout()

    # Create Table Widget for Well Data
        self.well_data_table = QTableWidget()
        self.well_data_table.setColumnCount(0)  # Initial column count
        self.well_data_table.setRowCount(0)      # Initial row count
        well_data_layout.addWidget(self.well_data_table)
        well_data_group.setLayout(well_data_layout)

    # Statistics Table Group
        statistics_group = self.create_group_box("Statistics", "#FCF3CF")
        statistics_layout = QHBoxLayout()

    # Table Widget for Statistics
        self.statistics_table = QTableWidget()
        self.statistics_table.setColumnCount(0)  # Initial column count for statistics
        self.statistics_table.setRowCount(0)      # Initial row count
        statistics_layout.addWidget(self.statistics_table)
        statistics_group.setLayout(statistics_layout)

    # Add Well Data and Statistics groups to the layout
        layout.addWidget(well_data_group)
        layout.addWidget(statistics_group)
    
        data_loading2_tab.setLayout(layout)
        return data_loading2_tab

    ###########################################
    ############################################
    ############Customizing the button style################
    def style_button(self, button):
        
        button.setStyleSheet("""QPushButton {
            background-color: purple;  
            color: white;                /* White text */
            border: none;                /* No border */
            border-radius:5px;         /* Rounded corners */
            padding: 10px;               /* Padding */
            font-size: 14px;             /* Font size */
            QPushButton:hover {
            background-color: yellow;}
            QPushButton:pressed {
            background-color: red;}
        """)
    #######################################################
    def create_visualization_tab(self):
        # Placeholder for the Basic Visualization tab content
        visualization_tab = QWidget()
        layout = QHBoxLayout()

    # Plotting Controls Section
        control_group_box = QGroupBox("Plotting Controls")
        control_layout = QVBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)  
        control_layout.setSpacing(5)  

    # Add buttons for different plots with icons and tooltips
        self.plot_buttons_layout = QVBoxLayout()
        self.plot_buttons_layout.setSpacing(5)
        # Create a helper method to create buttons
        def create_button(text, callback, tooltip):
            button=QPushButton(text)
            button.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 14px; } QPushButton:hover { background-color: #2980b9; }")
            button.clicked.connect(callback)
            button.setToolTip(tooltip)
            return button
        # Create buttons using the helper method
        self.histogram_button = create_button("Histogram", self.plot_histogram, "Generate Histogram Plot")
        self.scatter_plot_button = create_button("Scatter Plot", self.plot_scatter, "Generate Scatter Plot")
        self.cross_plot_button = create_button("Cross Plot", self.plot_cross, "Generate Cross Plot")
        self.triple_combo_plot_button = create_button("Triple Combo Plot", self.plot_triple_combo, "Generate Triple Combo Plot")
        self.formation_top_plot_button = create_button("Formation Top Plot", self.plot_formation_top, "Generate Formation Top Plot")

    # Add buttons to vertical layout
        self.plot_buttons_layout.addWidget(self.histogram_button)
        self.plot_buttons_layout.addWidget(self.scatter_plot_button)
        self.plot_buttons_layout.addWidget(self.cross_plot_button)
        self.plot_buttons_layout.addWidget(self.triple_combo_plot_button)
        self.plot_buttons_layout.addWidget(self.formation_top_plot_button)

    # Set layout for control group box
        control_group_box.setLayout(self.plot_buttons_layout)
        control_group_box.setStyleSheet("QGroupBox { font-weight: bold; }")  # Style group box header

    # Add control group box to main layout
        layout.addWidget(control_group_box)

    # Plot Display Section
        plot_group_box = QGroupBox("Plot Display Area")
        plot_layout = QVBoxLayout()
        self.canvas = FigureCanvas(plt.Figure())
        self.navtoolbar =  NavigationToolbar2QT(self.canvas)
        plot_layout.addWidget(self.navtoolbar)
        plot_layout.addWidget(self.canvas)
        plot_group_box.setLayout(plot_layout)
        
        
        ##########################
        #####################################
        # Create an instance of TripleComboPlot from Triplecombo.py
        self.triple_combo_plot = TripleComboPlot()

        # Add the plot to the layout of Basic Visualization tab
        layout.addWidget(self.triple_combo_plot)
        self.setLayout(layout)
        
        #####################################

    # Add plot group box to main layout
        layout.addWidget(plot_group_box)

    # Set fixed width for control group box to ensure buttons stay vertical and aligned
        control_group_box.setFixedWidth(200) 

    # Set spacing and margins for main layout
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

    # Set the layout for the visualization tab
        visualization_tab.setLayout(layout)

        return visualization_tab
    '''
    #-------------------------------------------------------------------------##########
    
                        GUI INTEGRATION
    
    ######----------------------------------------------------_______--------##########333333----------
    '''

    def create_visualization_tab(self):
        from visulization import Ui_Form  # Corrected module name
        from TripleCombo import TripleComboPlot  # Import TripleComboPlot
    
        # Create the visualization tab
        visualization_tab = QWidget()
        ui = Ui_Form()
        
        self.vis_ui = ui
        ui.setupUi(visualization_tab)
        self.visualization_tab = visualization_tab  # Corrected typo
        self.visualization_ui = ui  # Corrected typo
    
        # Set default values and connect buttons to functions
        self.visualization_ui.spinBox.setValue(10)
        self.visualization_ui.pushButton_2.clicked.connect(self.histogram)
        self.visualization_ui.pushButtoncross.clicked.connect(self.crossplot)
        self.visualization_ui.colorButton.clicked.connect(self.select_color)  # New button for color dialog
        self.visualization_ui.pushButton_plot_triple_combo.clicked.connect(self.plot_triple_combo)
    
        # Add the triple combo plot widget to a different part (scatter area)
        scatter_window = self.visualization_ui.tab_2  # Assuming scatter_tab is where the scatter plot resides
        scatter_layout = QVBoxLayout(scatter_window)  # Layout for the scatter plot section
    
        # Create an instance of the TripleComboPlot and add it to the scatter layout
        self.triple_combo_plot = TripleComboPlot()  # Instantiate the TripleComboPlot class
        scatter_layout.addWidget(self.triple_combo_plot)  # Add the plot to the layout
    
        # Optionally, store the instance if you need to access it later
        self.scatter_page = self.triple_combo_plot
        ############
        #Multitrack
        
        
        mlt_window=self.visualization_ui.tab_5
        layout=QVBoxLayout(mlt_window)
        mlt_page=VisulizationPage(self)
        layout.addWidget(mlt_page)
        self.mlt_page=mlt_page
        #################
        return visualization_tab
    
    def add_las_data_in_visulization(self):
        self.visualization_ui.comboBox.addItems(self.las_data.columns)
        self.visualization_ui.xcrosscomboBox.addItems(self.las_data.columns)
        self.visualization_ui.ycrosscomboBox.addItems(self.las_data.columns)
        self.visualization_ui.comboBox_GR.addItems(self.las_data.columns)
        self.visualization_ui.comboBox_RT.addItems(self.las_data.columns)
        self.visualization_ui.comboBox_NPHI.addItems(self.las_data.columns)
    

        
        self.mlt_page.set_dataframe_to_visualize(self.las_data)

    def histogram(self):
        
        # Check if the dataset and selected curve exist
        if hasattr(self, 'las_data'):
            curve_name = self.visualization_ui.comboBox.currentText()
            bin_count = self.visualization_ui.spinBox.value()
    
            if curve_name not in self.las_data.columns:
                raise KeyError(f"Curve {curve_name} not found in the dataset.")
    
            # Create Matplotlib Figure and Axes
            fig, ax = plt.subplots(figsize=(10, 6))
            counts, bins, patches = ax.hist(
                self.las_data[curve_name],
                bins=bin_count,
                edgecolor='black',
                alpha=0.7,
                color='skyblue'
            )
    
            # Add color gradient to bars for a better visual effect
            norm = plt.Normalize(min(counts), max(counts))
            sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
            sm.set_array([])
            for count, patch in zip(counts, patches):
                patch.set_facecolor(sm.to_rgba(count))
    
            # Add a color bar for frequency visualization
            cbar = fig.colorbar(sm, ax=ax)
            cbar.set_label('Frequency', fontsize=10)
    
            # Add interactivity: Display bin details on hover
            annot = ax.annotate(
                "", xy=(0, 0), xytext=(20, 20),
                textcoords="offset points",
                bbox=dict(boxstyle="round", fc="w"),
                arrowprops=dict(arrowstyle="->")
            )
            annot.set_visible(False)
    
            def update_annot(patch, count):
                x = (patch.get_x() + patch.get_width()) / 2
                annot.xy = (x, count)
                text = f"Bin Center: {x:.2f}\nFrequency: {count:.0f}"
                annot.set_text(text)
                annot.get_bbox_patch().set_alpha(0.9)
    
            def on_hover(event):
                if event.inaxes == ax:
                    for patch, count in zip(patches, counts):
                        if patch.contains(event)[0]:
                            update_annot(patch, count)
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                            return
                annot.set_visible(False)
                fig.canvas.draw_idle()
    
            fig.canvas.mpl_connect("motion_notify_event", on_hover)
    
            # Configure plot appearance
            ax.set_title(f"Histogram of {curve_name}", fontsize=14, weight='bold')
            ax.set_xlabel(curve_name, fontsize=12)
            ax.set_ylabel("Frequency", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
    
            # Embed Matplotlib Figure into PyQt5 widget
            canvas = FigureCanvas(fig)
            navi = NavigationToolbar2QT(canvas, self.visualization_tab)
    
            # Apply QSizePolicy to canvas and navigation toolbar
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            navi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    
            # Create a container widget for layout
            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(canvas)
            container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
            # Set the container widget in the scroll area
            self.visualization_ui.scrollArea.setWidget(container)
    
            
        # def crossplot(self):
        #     if hasattr(self,'las_data'):
        #         xcol = self.visualization_ui.xcrosscomboBox.currentText()
        #         ycol = self.visualization_ui.ycrosscomboBox.currentText()
        #         '''
        #         -------Select color for the scatter plot-------
                
        #         '''
        #         selected_palette = self.visualization_ui.crosscolorbox.currentText() 
        #         if selected_palette not in sns.color_palette():
        #             selected_palette = 'viridis'  # Default to 'viridis' if not found
        #         ## Check if selected columns are in the dataset
    #         if xcol not in self.las_data.columns or ycol not in self.las_data.columns:
    #             raise KeyError(f"Columns {xcol} or {ycol} not found in the dataset.")
    #         #################################
    #         fig, ax = plt.subplots(figsize=(10, 6))
    #         #ax.scatter(self.las_data[xcol], self.las_data[ycol], alpha=0.7, edgecolors='w')
    #         sns.scatterplot(x=xcol, y=ycol, data=self.las_data, palette=selected_palette, s=100, ax=ax, edgecolor='r', alpha=0.7)
            
            
    #         ax.set_xlabel(xcol,fontsize=12)
    #         ax.set_ylabel(ycol,fontsize=12)
    #         ax.set_title(f"Crossplot of {xcol} vs {ycol}")
    #         ax.grid(True, linestyle='--', alpha=0.6)
    #         plt.tight_layout()
    #         canvas = FigureCanvas(fig)
    #         navi = NavigationToolbar2QT(canvas, self.visualization_tab)
    #         container = QWidget()
    #         vlayout = QVBoxLayout(container)
    #         vlayout.addWidget(navi)
    #         vlayout.addWidget(canvas)
            
    #         self.visualization_ui.crossscrollArea.setWidget(container)
    def crossplot(self):
        
        if hasattr(self, 'las_data'):
            xcol = self.visualization_ui.xcrosscomboBox.currentText()
            ycol = self.visualization_ui.ycrosscomboBox.currentText()
    
            # Select color palette for scatter plot
            selected_palette = self.visualization_ui.crosscolorbox.currentText()
            if selected_palette not in sns.palettes.SEABORN_PALETTES:
                selected_palette = 'viridis'  # Default to 'viridis' if not found
    
            # Check if selected columns are in the dataset
            if xcol not in self.las_data.columns or ycol not in self.las_data.columns:
                raise KeyError(f"Columns {xcol} or {ycol} not found in the dataset.")
    
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = ax.scatter(
                self.las_data[xcol],
                self.las_data[ycol],
                c=np.arange(len(self.las_data)),  # Optional: Assign unique colors
                cmap=selected_palette,
                s=100,
                edgecolor='r',
                alpha=0.7
            )
            
            # Add color bar for clarity
           # cbar = fig.colorbar(scatter, ax=ax)
            #cbar.set_label('Index', fontsize=10)
    
            # Add hover functionality for displaying data points
            annot = ax.annotate(
                "", xy=(0, 0), xytext=(20, 20),
                textcoords="offset points",
                bbox=dict(boxstyle="round", fc="w"),
                arrowprops=dict(arrowstyle="->")
            )
            annot.set_visible(False)
    
            def update_annot(ind):
                pos = scatter.get_offsets()[ind["ind"][0]]
                annot.xy = pos
                text = f"{xcol}: {pos[0]:.2f}\n{ycol}: {pos[1]:.2f}"
                annot.set_text(text)
                annot.get_bbox_patch().set_alpha(0.9)
    
            def on_hover(event):
                if event.inaxes == ax:
                    cont, ind = scatter.contains(event)
                    if cont:
                        update_annot(ind)
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                    else:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()
    
            fig.canvas.mpl_connect("motion_notify_event", on_hover)
    
            # Configure plot appearance
            ax.set_xlabel(xcol, fontsize=12)
            ax.set_ylabel(ycol, fontsize=12)
            ax.set_title(f"Crossplot of {xcol} vs {ycol}", fontsize=14, weight='bold')
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
    
            # Embed Matplotlib figure into PyQt5 widget
            canvas = FigureCanvas(fig)
            navi = NavigationToolbar2QT(canvas, self.visualization_tab)
    
            # Apply QSizePolicy to canvas and navigation toolbar
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            navi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    
            # Create a container widget for layout
            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(canvas)
            container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
            # Set the container widget in the scroll area
            self.visualization_ui.crossscrollArea.setWidget(container)


        
        """
--------------------------------------------------------------------
FUNCTION FOR COLOR DIALOG 

-------------------------------------------------------------------
        """

    def select_color(self):
        
        # Open a QColorDialog to select a color
        color = QColorDialog.getColor()

        if color.isValid():
            self.scatter_color = color.name()  # Save the selected color
 
        
        """_
        -----------------------------
        
        TRIPLE COMBO PLOT
        
        ------------------------------
        """
    def plot_triple_combo(self):
        
        if self.las_data is None:
            print("Error: No data uploaded.")
            return

        # Retrieve selected options from the checkable combo boxes
        gr_options = self.vis_ui.comboBox_GR.getSelectedItems()
        # gr_options = [gr_items.itemText(index) for index in range(gr_items.count()) 
        #               if gr_items.itemData(index, Qt.CheckStateRole) == Qt.CheckState.Checked]
    
        resistivity_options = self.vis_ui.comboBox_RT.getSelectedItems()
        # resistivity_options = [resistivity_items.itemText(index) for index in range(resistivity_items.count()) 
        #                        if resistivity_items.itemData(index, Qt.CheckStateRole) == Qt.CheckState.Checked]
    
        porosity_options = self.vis_ui.comboBox_NPHI.getSelectedItems()
        # porosity_options = [porosity_items.itemText(index) for index in range(porosity_items.count()) 
        #                     if porosity_items.itemData(index, Qt.CheckStateRole) == Qt.CheckState.Checked]
    
        # Print selected options (optional, for debugging)
        print("Selected GR Logs: ", gr_options)
        print("Selected Resistivity Logs: ", resistivity_options)
        print("Selected Porosity Logs: ", porosity_options)
    
        # porosity_items = self.vis_ui.comboBox_NPHI.getSelectedItems()
        porosity_options = self.vis_ui.comboBox_NPHI.getSelectedItems()
        # self.vis_ui.comboBox_GR.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.vis_ui.comboBox_RT.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.vis_ui.comboBox_NPHI.setSelectionMode(QAbstractItemView.MultiSelection)    
    
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
    
        # Initialize the plot
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 12))
    
        # Gamma Ray and Caliper track - Plot on the same graph
        for gr_curve in gr_options:
            if gr_curve != "CALI":
                ax1.plot(well[gr_curve], well["DEPTH"], label=f"Gamma Ray: {gr_curve}", color="green")
                ax1.fill_betweenx(well["DEPTH"], well["GR"], 0, where=(well["GR"] > 0), facecolor='green', alpha=0.3)

        # Configure primary x-axis for Gamma Ray
        ax1.xaxis.label.set_color("green")
        ax1.set_xlim(0, 200)
        ax1.set_ylabel("Depth (m)")
        ax1.set_xlabel("Gamma Ray")
        ax1.tick_params(axis='x', colors="green")
        ax1.spines["top"].set_edgecolor("green")
        ax1.spines['top'].set_position(('axes', 1.02))
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
        ax1_twin.spines['top'].set_position(('axes', 1.07))
        ax1_twin.spines['top'].set_visible(True)
        ax1_twin.legend()
    
        # Set depth range for both axes
        ax1.set_ylim(well["DEPTH"].max(), well["DEPTH"].min())  # Depth should decrease downward
        ax1_twin.set_ylim(well["DEPTH"].max(), well["DEPTH"].min())
    
        ## Resistivity track - Plot all selected resistivity columns on the same plot
        # Resistivity track - Plot all selected resistivity columns on the same plot using twin axes
        for i, resistivity_curve in enumerate(resistivity_options):
            if i == 0:
                # Plot the first resistivity log on the primary x-axis
                ax2.plot(well[resistivity_curve], well["DEPTH"], label=resistivity_curve, color=f"C{i}")
                curve_min = well[resistivity_curve].min()
                curve_max = well[resistivity_curve].max()
                ax2.set_xlim(curve_min - (curve_max - curve_min) * 0.1, 
                             curve_max + (curve_max - curve_min) * 0.1)  # Add 10% margin
                ax2.set_xlabel(f"{resistivity_curve} ", color=f"C{i}")
                ax2.tick_params(axis='x', colors=f"C{i}")
                ax2.spines['top'].set_edgecolor(f"C{i}")
            else:
                # Create a twin x-axis for additional resistivity logs
                twin_ax = ax2.twiny()
                twin_ax.plot(well[resistivity_curve], well["DEPTH"], label=resistivity_curve, color=f"C{i}", linestyle="--")
                curve_min = well[resistivity_curve].min()
                curve_max = well[resistivity_curve].max()
                twin_ax.set_xlim(curve_min - (curve_max - curve_min) * 0.1, 
                                 curve_max + (curve_max - curve_min) * 0.1)  # Add 10% margin
                twin_ax.set_xlabel(f"{resistivity_curve} ", color=f"C{i}")
                twin_ax.tick_params(axis='x', colors=f"C{i}")
                twin_ax.spines['top'].set_edgecolor(f"C{i}")
                twin_ax.spines["top"].set_position(("axes", 1.0 + 0.07 * i))  # Offset for multiple axes
        ax2.xaxis.set_ticks_position("top")
        ax2.xaxis.set_label_position("top")
        ax2.set_ylim(max(well["DEPTH"]), min(well["DEPTH"]))  # Ensure depth increases downward
        ax2.grid(which='major', color='lightgrey', linestyle='-')
        ax2.legend()

        # Porosity track - Plot all selected porosity columns on the same plot using twin axes
        for i, porosity_curve in enumerate(porosity_options):
            
            # Determine color and style for visibility
            line_color = f"C{i}"
            line_style = "-" if porosity_curve == "RHOB" else "--"
            line_width = 1 if porosity_curve == "RHOB" else 0.8
        
            curve_min = well[porosity_curve].min()
            curve_max = well[porosity_curve].max()
            
            # Add margin for clarity
            margin = 0.1 * (curve_max - curve_min)
            curve_min -= margin
            curve_max += margin
        
            if i == 0:
                # Plot the first porosity log on the primary x-axis
                ax3.plot(well[porosity_curve], well["DEPTH"], label=porosity_curve, color=line_color, linestyle=line_style, linewidth=line_width)
        
                # Set x-axis limits
                if porosity_curve == "RHOB":
                    ax3.set_xlim(curve_min, curve_max)
                else:
                    ax3.set_xlim(curve_max, curve_min)
        
                ax3.set_xlabel(f"{porosity_curve}", color=line_color)
                ax3.tick_params(axis='x', colors=line_color)
                ax3.spines['top'].set_edgecolor(line_color)
            else:
                # Create a twin x-axis for additional porosity logs
                twin_ax = ax3.twiny()
                twin_ax.plot(well[porosity_curve], well["DEPTH"], label=porosity_curve, color=line_color, linestyle=line_style, linewidth=line_width)
        
                # Set x-axis limits
                if porosity_curve == "RHOB":
                    twin_ax.set_xlim(curve_min, curve_max)
                else:
                    twin_ax.set_xlim(curve_max, curve_min)
        
                twin_ax.set_xlabel(f"{porosity_curve}", color=line_color)
                twin_ax.tick_params(axis='x', colors=line_color)
                twin_ax.spines['top'].set_edgecolor(line_color)
                twin_ax.spines["top"].set_position(("axes", 1.0 + 0.1 * i))  # Increased offset for readability
        
# Gl        obal settings
        ax3.xaxis.set_ticks_position("top")
        ax3.xaxis.set_label_position("top")
        ax3.set_ylim(max(well["DEPTH"]), min(well["DEPTH"]))  # Ensure depth increases downward
        ax3.grid(which='major', color='lightgrey', linestyle='-', alpha=0.5)
        ax3.legend(loc="upper left", fontsize="small")  # Adjust legend location and size


        
    
        # Common functions for setting up the plot can be extracted into
        # a loop to avoid repeating code
        for ax in [ax1, ax2, ax3]:
            ax.set_ylim(max(well["DEPTH"]), min(well["DEPTH"]))  # Depth increases downwards
            ax.grid(which='major', color='lightgrey', linestyle='-')
            ax.xaxis.set_ticks_position("top")
            ax.xaxis.set_label_position("top")
            ax.spines["top"].set_position(("axes", 1.0))
    
        plt.tight_layout()
        canvas = FigureCanvas(fig)
        navi = NavigationToolbar2QT(canvas, self.visualization_tab)
        container = QWidget()
        vlayout = QVBoxLayout(container)
        vlayout.addWidget(navi)
        vlayout.addWidget(canvas)
        self.vis_ui.scrollArea_2.setWidget(container)
    
    
    
    ################################### ###################
#############   Create formation evaluation tab   #################
    def create_formation_evaluation_tab(self):
        # Enhanced Formation Evaluation Tab
        formation_evaluation_tab = QWidget()
        layout = QGridLayout()

    # Title
        title_label = QLabel("Formation Evaluation: Vshale Calculation and Plot")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("padding: 10px; color: #2E8B57;")
        layout.addWidget(title_label, 0, 0, 1, 2)

    # Vshale Type Selection
        vshale_group = QGroupBox("Vshale Calculation Method")
        vshale_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        vshale_layout = QVBoxLayout()
        vshale_layout.addWidget(QLabel("Select the Vshale method:"))
        self.vshape_combobox = QComboBox()
        self.vshape_combobox.addItems(["Linear", "Larionov Older Rock", "Larionov Tertiary Rock", "Clavier"])
        vshale_layout.addWidget(self.vshape_combobox)
        vshale_group.setLayout(vshale_layout)
        layout.addWidget(vshale_group, 1, 0)

        formation_evaluation_tab.setLayout(layout)
        return formation_evaluation_tab
    
    
    '''
    #-------------------------------------------------------------------------##########
    
                        GUI INTEGRATION
    
    ######----------------------------------------------------_______--------##########333333----------
    '''
    def create_formation_evaluation_tab(self):
        from formationUI import Ui_Form  # Corrected module name
        formation_evaluation_tab = QWidget()
        ui = Ui_Form()
        ui.setupUi(formation_evaluation_tab)
        self.formation_evaluation_tab = formation_evaluation_tab  # Corrected typo
        self.formationGUI_ui = ui  # Corrected typo
        # self.formationGUI_ui.grmin.value()
        
        # self.formationGUI_ui.grmax.value()
        #self.formationGUI_ui.Shaletype.setCurrentText()
        self.formationGUI_ui.vsub.clicked.connect(self.vsub)
        #self.formationGUI_ui.porosub.clicked.connect(self.porosity_plot)
        self.formationGUI_ui.porosub_2.clicked.connect(self.water_saturation)
        self.formationGUI_ui.NPHIsub.clicked.connect(self.neutron_porosity_plot)
        self.formationGUI_ui.dphisub.clicked.connect(self.dphi_plot)
        self.formationGUI_ui.tphieffecsub.clicked.connect(self.total_neutron_plot)
        self.formationGUI_ui.flagsub.clicked.connect(self.reservoir_ntg_flag)
        #self.formationGUI_ui.nanremsub.clicked.connect(self.vshale_plot)
        
        
        ##############  QC##############
        self.formationGUI_ui.Outlierremovesub.clicked.connect(self.outlier_removal)
        self.formationGUI_ui.bitsizeholdedevsub.clicked.connect(self.bitsize_variation)
        self.formationGUI_ui.nanlinear.clicked.connect(self.nan_removal)
        self.formationGUI_ui.nanmean.clicked.connect(self.nan_removal)
        return formation_evaluation_tab
    
    
    # ADD DATA 
    def add_las_data_in_formation_evaluation(self):        
        self.formationGUI_ui.NPHILOG.addItems(self.las_data.columns)
        self.formationGUI_ui.outlierremsellog.addItems(self.las_data.columns)
        #self.formationGUI_ui.nanlinear.addItems(self.las_data.columns)
        #self.formationGUI_ui.nanremselcurve.addItems(self.las_data.columns)
    



#--------------------------------------------------------------------------------

                    #  QUALITY CONTROL
                    
#-------------------------------------------------------------------------------------"""    
# Building an Isolation Forest Model (2 Features)

    def outlier_removal(self):
        
        try:
            # Select column for anomaly detection
            anomaly_input = self.formationGUI_ui.outlierremsellog.currentText()
            if anomaly_input not in self.las_data:
                QMessageBox.warning(self, "Error", f"Column '{anomaly_input}' not found in data.")
                return
    
            # Ensure column is numeric and drop NaN values
            data = self.las_data[anomaly_input].dropna()
            if data.empty:
                QMessageBox.warning(self, "Error", "Selected column has no valid data after removing NaN values.")
                return
    
            if not np.issubdtype(data.dtype, np.number):
                QMessageBox.warning(self, "Error", f"Column '{anomaly_input}' contains non-numeric values.")
                return
    
            # Check for 'DEPTH' or 'dept' column
            depth_column = None
            if 'DEPTH' in self.las_data:
                depth_column = 'DEPTH'
            elif 'DEPT' in self.las_data:
                depth_column = 'DEPT'
            else:
                QMessageBox.warning(self, "Error", "Neither 'DEPTH' nor 'dept' column found in data.")
                return
    
            # Prepare data for Isolation Forest
            data_reshaped = data.values.reshape(-1, 1)
            model_IF = IsolationForest(contamination=0.1, random_state=42)
            model_IF.fit(data_reshaped)
            
            # Map anomaly predictions back to original dataset (fill dropped rows with NaN)
            self.las_data['anomaly'] = np.nan
            self.las_data.loc[data.index, 'anomaly'] = model_IF.predict(data_reshaped)
    
            # Debugging: Check results
            print("Anomaly counts:", self.las_data['anomaly'].value_counts())
    
            # Plot the anomalies
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(
                x=self.las_data[anomaly_input],
                y=self.las_data[depth_column],
                hue=self.las_data['anomaly'],
                palette={1: '#1f77b4', -1: '#ff7f0e'},
                alpha=0.7,
                ax=ax
            )
            ax.set_title(f"Outlier Detection: {anomaly_input}")
            ax.set_xlabel(anomaly_input)
            ax.set_ylabel(depth_column)
            ax.legend(title="Anomaly", labels=["Inlier", "Outlier"])
            
            ax.invert_yaxis()
    
            # Display the plot in GUI
            # Add plot and navigation toolbar to a container widget
            canvas_outlier = FigureCanvas(fig)
            plt.tight_layout()            
            navi = NavigationToolbar2QT(canvas_outlier, self.formation_evaluation_tab)    
        
            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(canvas_outlier)
        
            # Set the container widget in the QScrollArea
            self.formationGUI_ui.outlierremplot.setWidget(container)
    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
            print(f"Error details: {e}")


    ######################### Bit size variation ####################  
    
    def bitsize_variation(self):
        try:
            
            # Get user inputs
            choose_bit = float(self.formationGUI_ui.bitsize.value())
            tolerance_limit = float(self.formationGUI_ui.holedev.value())
    
            # Calculate tolerance and add it as a new column
            self.las_data['tolerance'] = abs(self.las_data['CALI'] - choose_bit)
    
            # Filter rows with bad data (tolerance greater than the limit)
            bad_data = self.las_data[self.las_data['tolerance'] > tolerance_limit]
    
            # Check if bad data exists
            if bad_data.empty:
                QMessageBox.information(self, "No Bad Data", "No rows with tolerance greater than the limit found.")
                return
    
            # Display the bad data in the scroll area
            self.show_bad_data_in_scroll_area(bad_data)

        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {e}")
        except KeyError as e:
            QMessageBox.warning(self, "Error", f"Missing column in data: {e}")
        
        def show_bad_data_in_scroll_area(self, bad_data):
            # Create a QTableWidget
            rows, cols = bad_data.shape
            table_widget = QTableWidget(rows, cols)
            table_widget.setHorizontalHeaderLabels(bad_data.columns)
        
            # Populate the table with bad data
            for i, row in bad_data.iterrows():
                for j, col in enumerate(bad_data.columns):
                    table_widget.setItem(i, j, QTableWidgetItem(str(row[col])))
        
            # Adjust table settings
            table_widget.resizeColumnsToContents()
            table_widget.resizeRowsToContents()
        
            # Clear the scroll area first
            scroll_area_layout = self.formationGUI_ui.badDataScrollArea.widget().layout()
            if scroll_area_layout is not None:
                for i in reversed(range(scroll_area_layout.count())):
                    widget = scroll_area_layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()
        
            # Add the table widget to the scroll area
            layout = QVBoxLayout()
            layout.addWidget(table_widget)
        
            container = QWidget()
            container.setLayout(layout)
        
            self.formationGUI_ui.badDataScrollArea.setWidget(container)

    
        
#################### nan removal########################

    
    def nan_removal(self):
        try:
            # Check if the 'las_data' DataFrame has any missing values
            if self.las_data.isnull().sum().sum() == 0:
                QMessageBox.warning(self, "Info", "No missing values in the dataset.")
                return
            
            # Apply the NaN removal method based on the selected radiobutton
            if self.formationGUI_ui.nanlinear.isChecked():
                self.las_data = self.las_data.interpolate(method='linear')  # Linear interpolation
            elif self.formationGUI_ui.nanmean.isChecked():
                self.las_data = self.las_data.fillna(self.las_data.mean())  # Fill NaN with column mean
            else:
                QMessageBox.warning(self, "Error", "Please select a NaN removal method.")
                return
            
            # Visualize missing data using missingno
            data_nan = self.las_data
            fig = plt.figure(figsize=(10, 6))  # Adjust the figure size
            
            # Create a missing data matrix plot
            msno.matrix(data_nan, ax=fig.add_subplot(111))
            
            # Display the plot
            canvas_nan = FigureCanvas(fig)
            plt.tight_layout()  # Adjust the layout of the plot
            
            # Add navigation toolbar
            navi = NavigationToolbar2QT(canvas_nan, self.formation_evaluation_tab)
            
            # Create a container widget to hold the plot and toolbar
            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(canvas_nan)
            
            # Set the container widget in the QScrollArea
            self.formationGUI_ui.nanremplot.setWidget(container)
        
        except Exception as e:
            # Handle any unexpected errors
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
            print(f"Error details: {e}")
    
    

##############################################
###################Vshale calculation##########



    # def vsub(self):
    #     method = self.formationGUI_ui.Shaletype.currentText()
    #     min_gr = float(self.formationGUI_ui.grmin.value())  # Convert to float
    #     max_gr = float(self.formationGUI_ui.grmax.value())  # Convert to float
    
    #     gr_data = self.las_data["GR"]  # Assuming 'GR' column exists in the DataFrame
    #     ####
    #     p_5 = np.percentile(gr_data, 5)
    #     p_95 = np.percentile(gr_data, 95)
        
    #     ######
    #     # Calculate Vshale
    #     vshale_linear = (gr_data - min_gr) / (max_gr - min_gr)
        
    #     if method == "Linear":
    #         vshale = vshale_linear
    #     elif method == "Vsh_Larinor_Tertiary":
    #         vshale = 0.083 * (2 ** (3.7 * vshale_linear) - 1)
    #     elif method == "Vsh_Larinor_older":
    #         vshale = 0.33 * (2 ** (2 * vshale_linear) - 1)
    #     elif method == "Vsh_Clavier":
    #         vshale = 1.7 - np.sqrt(3.38 - (vshale_linear + 0.7) ** 2)
    #     else:
    #         QMessageBox.warning(self, "Error", "Invalid Vshale calculation method selected.")
    #         return
        
    #     # Plot Gamma Ray and Vshale side by side (horizontally)
    #     fig, (ax1, ax2) = plt.subplots(figsize=(1, 8), nrows=1, ncols=2)
    
    #     # Gamma Ray plot (on the first track/left side)
    #     ax1.plot(gr_data, self.las_data['DEPTH'], color='green', label='Gamma Ray')
    #     ax1.set_xlabel("Gamma Ray")
    #     ax1.set_ylabel("Depth")
    #     ax1.set_xlim(0, 200)  # Set the x-axis limit for Gamma Ray plot
    #     ax1.xaxis.set_label_position('top')  # Move the x-axis labels to the top
    #     ax1.invert_yaxis()  # Depth increases downward
    #     ax1.legend()
    #     ax1.grid(True)
    #     #ax1.set_title('Gamma Ray')
    #     # Add vertical lines for 5th and 95th percentiles
    #     ax1.axvline(p_5, color='red', linestyle='--', label=f'P5: {p_5:.2f}')
    #     ax1.axvline(p_95, color='blue', linestyle='--', label=f'P95: {p_95:.2f}')
    #     ax1.legend(loc='upper right')  # Show legend in the upper left
    
    
    #     # Vshale plot (on the second track/right side)
    #     ax2.plot(vshale, self.las_data['DEPTH'], color='blue', label=f'Vshale ({method})')
    #     ax2.set_xlabel("Vshale")
    #     ax2.set_ylabel("Depth")
    #     ax2.invert_yaxis()  # Depth increases downward
    #     ax2.legend()
    #     ax2.grid(True)
    #    # ax2.set_title('Vshale Calculation')
    
    #     # Set the canvas to display the figure
    #     vshale_canvas = FigureCanvas(fig)

    #     plt.tight_layout()
    #     navi = NavigationToolbar2QT(vshale_canvas, self.formation_evaluation_tab)
    #     #canvas = FigureCanvas(fig)
    #     #navi = NavigationToolbar2QT(canvas, self.formation_tab)
    #     #container = QWidget()
    #     #vlayout = QVBoxLayout(container)
    #     #vlayout.addWidget(navi)
    #     #vlayout.addWidget(canvas)
    #     ##self.vis_ui.vplot.setWidget(container)
    #     container = QWidget()
    #     vlayout = QVBoxLayout(container)
    #     vlayout.addWidget(navi)
    #     vlayout.addWidget(vshale_canvas)
    #     self.formationGUI_ui.vplot.setWidget(vshale_canvas)
    def vsub(self):
        
        method = self.formationGUI_ui.Shaletype.currentText()
        min_gr = float(self.formationGUI_ui.grmin.value())  # Convert to float
        max_gr = float(self.formationGUI_ui.grmax.value())  # Convert to float
    
        gr_data = self.las_data["GR"]  # Assuming 'GR' column exists in the DataFrame
        
        # Percentile calculations
        p_5 = np.percentile(gr_data, 5)
        p_95 = np.percentile(gr_data, 95)
    
        # Calculate Vshale
        vshale_linear = (gr_data - min_gr) / (max_gr - min_gr)
        
        if method == "Linear":
            vshale = vshale_linear
        elif method == "Vsh_Larinor_Tertiary":
            vshale = 0.083 * (2 ** (3.7 * vshale_linear) - 1)
        elif method == "Vsh_Larinor_older":
            vshale = 0.33 * (2 ** (2 * vshale_linear) - 1)
        elif method == "Vsh_Clavier":
            vshale = 1.7 - np.sqrt(3.38 - (vshale_linear + 0.7) ** 2)
        else:
            QMessageBox.warning(self, "Error", "Invalid Vshale calculation method selected.")
            return
        
        # Plot Gamma Ray and Vshale side by side
        fig, (ax1, ax2) = plt.subplots(figsize=(6, 8), nrows=1, ncols=2)  # Adjust width for better visibility
    
        # Gamma Ray plot
        ax1.plot(gr_data, self.las_data['DEPTH'], color='green', label='Gamma Ray')
        ax1.set_xlabel("Gamma Ray")
        ax1.set_ylabel("Depth")
        ax1.set_xlim(0, 200)  # Set the x-axis limit for Gamma Ray plot
        ax1.xaxis.set_label_position('top')
        ax1.invert_yaxis()  # Depth increases downward
        ax1.axvline(p_5, color='red', linestyle='--', label=f'P5: {p_5:.2f}')
        ax1.axvline(p_95, color='blue', linestyle='--', label=f'P95: {p_95:.2f}')
        ax1.legend(loc='upper right')
        ax1.grid(True)
    
        # Vshale plot
        ax2.plot(vshale, self.las_data['DEPTH'], color='blue', label=f'Vshale ({method})')
        ax2.set_xlabel("Vshale")
        ax2.set_ylabel("Depth")
        ax2.invert_yaxis()
        ax2.legend()
        ax2.grid(True)
    
        # Set the canvas to display the figure
        vshale_canvas = FigureCanvas(fig)
        plt.tight_layout()
    
        # Navigation toolbar for the plot
        navi = NavigationToolbar2QT(vshale_canvas, self.formation_evaluation_tab)
    
        # Add plot and navigation toolbar to a container widget
        container = QWidget()
        vlayout = QVBoxLayout(container)
        vlayout.addWidget(navi)
        vlayout.addWidget(vshale_canvas)
    
        # Set the container widget in the QScrollArea
        self.formationGUI_ui.vplot.setWidget(container)
    
    
            
#"""--------------------------------------------------------------------------------

    #                       PLOTTING porosity
    
#-----------------------------------------------------------------------------------"""
    def neutron_porosity_plot(self):
        
        try:
            # Get the selected log (column) name from the GUI
            phi_N_key = self.formationGUI_ui.NPHILOG.currentText()
            
            # Ensure the selected column exists in self.las_data
            if phi_N_key not in self.las_data:
                QMessageBox.warning(self, "Error", f"Column '{phi_N_key}' not found in data.")
                return
            
            # Retrieve the selected log data from self.las_data
            phi_N = self.las_data[phi_N_key]
            
            # Get correction inputs
            correction_method = self.formationGUI_ui.MATCORR.currentText()
            correction = self.formationGUI_ui.CORRVAL.value()  # Correction value (float)
    
            # Apply SHALE correction based on the selected method
            if correction_method == "Addition":
                phi_N_corr = phi_N + correction
            elif correction_method == "Substraction":
                phi_N_corr = phi_N - correction
            else:
                QMessageBox.warning(self, "Error", "Invalid correction method selected.")
                return
    
            # Plot Corrected Porosity with Depth
            fig, ax = plt.subplots(figsize=(4, 6))  # Adjust figure size for better visibility
    
            # Plot Corrected Porosity
            ax.plot(phi_N_corr, self.las_data['DEPTH'], color='blue', label="TNPH Corrected")
            ax.set_xlabel(f"{phi_N_key}")
            ax.set_ylabel("Depth")
            ax.set_xlim(phi_N.min(), phi_N.max())  # Set x-axis limits based on data range
            ax.xaxis.set_label_position('top')  # Move the x-axis label to the top
            ax.invert_yaxis()  # Depth increases downward
            ax.legend(loc="upper right")  # Adjusted legend position
            ax.grid(True)
    
            # Render the plot in the PyQt GUI
            neutron_porosity_canvas = FigureCanvas(fig)
            plt.tight_layout()  # Adjust the layout to avoid clipping
            navi = NavigationToolbar2QT(neutron_porosity_canvas, self.formation_evaluation_tab)
    
            # Create a container widget and add the plot and navigation toolbar
            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(neutron_porosity_canvas)
    
            # Set the container widget in the QScrollArea
            self.formationGUI_ui.nphiplot.setWidget(container)
    
        except ValueError as e:
            # Handle cases where numerical conversion fails
            QMessageBox.warning(self, "Input Error", f"Invalid numerical input: {e}")
        except KeyError as e:
            # Handle missing data in the LAS file
            QMessageBox.warning(self, "Data Error", f"Missing key in LAS data: {e}")
    
                
    
####    ############################################
               #Density POROSITY

#############################################
        #phi_total = (phi_N + phi_D) / 2
    def dphi_plot(self):
        try: 
            rho_ma=self.formationGUI_ui.rhoma.value()
            rho_fl=self.formationGUI_ui.rhof.value()
            rho_bulk=self.las_data['RHOB']
            rho_den=(rho_ma-rho_bulk)/(rho_ma-rho_fl)
            
            #Plot the density porosity
            # Plot Corrected Porosity with Depth
            fig, ax = plt.subplots(figsize=(4, 6))  # Adjusted figure size for better visibility
    
            # Plot Corrected Porosity
            ax.plot(rho_den, self.las_data['DEPTH'], color='blue', label="Plot of Density Porosity")
            ax.set_xlabel("Density Porosity")
            ax.set_ylabel("Depth")
            ax.set_xlim(rho_den.min(), rho_den.max())  # Set x-axis limit (adjust as needed for your data range)
            ax.xaxis.set_label_position('top')  # Move the x-axis labels to the top
            ax.invert_yaxis()  # Depth increases downward
            ax.legend(loc="upper right")  # Adjusted legend position
            ax.grid(True)
    
            # Display the plot
            plt.tight_layout()
    
            # Set the canvas to display the figure
            density_porosity_canvas = FigureCanvas(fig)
            plt.tight_layout()
            
            navi = NavigationToolbar2QT(density_porosity_canvas, self.formation_evaluation_tab)
            
            # Add plot and navigation toolbar to a container widget
            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(density_porosity_canvas)
        
            # Set the container widget in the QScrollArea
            self.formationGUI_ui.dphiplot.setWidget(container)
            
            
            
        except ValueError as e:
            # Handle the case where conversion to float fails
            QMessageBox.warning(self, "Input Error", f"Invalid numerical input: {e}")
        except KeyError as e:
            # Handle missing data in LAS file
            QMessageBox.warning(self, "Data Error", f"Missing key in LAS data: {e}")
        
################################################################################################

                         #Total_neutron_plot

####################################################################################################

    def total_neutron_plot(self):
        porosity_type = self.formationGUI_ui.tphieffecselect.currentText()
    
        # Get the selected log (column) name from the GUI
        phi_N_key = self.formationGUI_ui.NPHILOG.currentText()
        
        # Ensure the selected column exists in self.las_data
        if phi_N_key not in self.las_data:
            QMessageBox.warning(self, "Error", f"Column '{phi_N_key}' not found in data.")
            return
        
        # Retrieve the selected log data from self.las_data
        phi_N = self.las_data[phi_N_key]
        
        # Convert inputs to appropriate types
        correction_method = self.formationGUI_ui.MATCORR.currentText()
        correction = self.formationGUI_ui.CORRVAL.value()  # correction is already a float
        
        # Apply SHALE correction based on the selected method
        if correction_method == "Addition":
            phi_N_corr = phi_N + correction
        elif correction_method == "Substraction":
            phi_N_corr = phi_N - correction
        else:
            QMessageBox.warning(self, "Error", "Invalid correction method selected.")
            return
        
        phi_N1 = phi_N_corr
        
        # Additional required parameters
        rho_ma = self.formationGUI_ui.rhoma.value()
        rho_fl = self.formationGUI_ui.rhof.value()
        rho_bulk = self.las_data['RHOB']
        rho_den = (rho_ma - rho_bulk) / (rho_ma - rho_fl)
        
        # Retrieve Vshale calculation method
        method = self.formationGUI_ui.Shaletype.currentText()
        min_gr = float(self.formationGUI_ui.grmin.value())  # Convert to float
        max_gr = float(self.formationGUI_ui.grmax.value())  # Convert to float
        
        gr_data = self.las_data["GR"]  # Assuming 'GR' column exists in the DataFrame
        
        # Calculate percentiles for Gamma Ray
        p_5 = np.percentile(gr_data, 5)
        p_95 = np.percentile(gr_data, 95)
        
        # Calculate Vshale using the selected method
        vshale_linear = (gr_data - min_gr) / (max_gr - min_gr)
        
        if method == "Linear":
            vshale = vshale_linear
        elif method == "Vsh_Larinor_Tertiary":
            vshale = 0.083 * (2 ** (3.7 * vshale_linear) - 1)
        elif method == "Vsh_Larinor_older":
            vshale = 0.33 * (2 ** (2 * vshale_linear) - 1)
        elif method == "Vsh_Clavier":
            vshale = 1.7 - np.sqrt(3.38 - (vshale_linear + 0.7) ** 2)
        else:
            QMessageBox.warning(self, "Error", "Invalid Vshale calculation method selected.")
            return
        
        # Calculate total porosity or effective porosity based on the selected type
        phi_d = rho_den
        if porosity_type == "TPHI":
            total_phi = np.sqrt(((phi_N1) ** 2) + ((phi_d) ** 2) / 2)
            # Only plot total porosity
            effective_por = None  # Set to None to avoid plotting it
        elif porosity_type == "Effective Porosity":
            effective_por = phi_N1 * (1 - vshale)  # Corrected from `total_phi(1 - vshale)`
            total_phi = None  # Set to None to avoid plotting it
        else:
            QMessageBox.warning(self, "Error", "Invalid porosity type selected.")
            return
        
        # Plotting the results
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if total_phi is not None:
            ax.plot(total_phi, self.las_data['DEPTH'], color='green', label='Total Porosity')
            ax.set_xlabel("Total Porosity")
            ax.xaxis.set_label_position('top')  # Move the x-axis labels to the top
            ax.set_xlim(total_phi.min(), total_phi.max()) 
            ax.set_title('Total Porosity')


        if effective_por is not None:
            ax.plot(effective_por, self.las_data['DEPTH'], color='blue', label='Effective Porosity')
            ax.set_xlabel("Effective Porosity")
            ax.xaxis.set_label_position('top')  # Move the x-axis labels to the top
            ax.set_xlim(effective_por.min(), effective_por.max())
            ax.set_title('Effective Porosity')
            
        ax.set_ylabel("Depth")
        ax.invert_yaxis()  # Depth increases downward
        ax.legend()
        ax.grid(True)
        
        # Set the canvas to display the figure
        total_poros_canvas = FigureCanvas(fig)
        plt.tight_layout()
        navi = NavigationToolbar2QT(total_poros_canvas, self.formation_evaluation_tab)
        
        container = QWidget()
        vlayout = QVBoxLayout(container)
        vlayout.addWidget(navi)
        vlayout.addWidget(total_poros_canvas)
        self.formationGUI_ui.tphieffecplot.setWidget(container)
    

            
####    ##############################################################################################
#"""    --------------------------------------------------------------------------------
    
        #                       PLOTTING WATER SATURATION
    
#-----------------------------------------------------------------------------------"""

    def water_saturation(self):
        try:
            # Convert QLineEdit inputs to float
            a = float(self.formationGUI_ui.Rwvalue.text())  # Conversion to float
            m = float(self.formationGUI_ui.mvalue.text())
            n = float(self.formationGUI_ui.nvalue.text())
            porosity = float(self.formationGUI_ui.Porosityvalue.text())
            rw = float(self.formationGUI_ui.Rwvalue.text())
            
            # Calculate water saturation
            water_sat = np.sqrt((a * rw) / ((porosity ** m) * self.las_data['RT']))
            
            # Plot Water Saturation with Depth
            fig, ax = plt.subplots(figsize=(2, 4))
            
            # Plot Water Saturation
            ax.plot(water_sat, self.las_data['DEPTH'], color='blue', label='Water Saturation')
            ax.set_xlabel("Water Saturation")
            ax.set_ylabel("Depth")
            ax.set_xlim(0, 1)  # Set x-axis limit for Water Saturation (from 0 to 1)
            ax.xaxis.set_label_position('top')  # Move the x-axis labels to the top
            ax.invert_yaxis()  # Depth increases downward
            ax.legend()
            ax.grid(True)
            
            # Display the plot
            plt.tight_layout()
            
            # Set the canvas to display the figure
            water_sat_canvas = FigureCanvas(fig)
            plt.tight_layout()
            navi = NavigationToolbar2QT(water_sat_canvas, self.formation_evaluation_tab)

            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(water_sat_canvas)
        
            # Set the container widget in the QScrollArea
            self.formationGUI_ui.watersatplot.setWidget(container)
            
        except ValueError as e:
            # Handle the case where conversion fails
            QMessageBox.warning(self, "Input Error", f"Invalid numerical input: {e}")
        except KeyError as e:
            QMessageBox.warning(self, "Data Error", f"Missing key in LAS data: {e}")
######################################################################################################
#                    Reservoir_ntg_flag

    def reservoir_ntg_flag(self):
        try:
            min_depth=float(self.formationGUI_ui.flagdepthmin.text())
            max_depth=float(self.formationGUI_ui.flagdepthmax.text())
            vsh_th = float(self.formationGUI_ui.flagvsh.text())  # Conversion to float
            sw_th = float(self.formationGUI_ui.flagsw.text())
            phi_eff_th= float(self.formationGUI_ui.flagporocut.text())
            
            # Calculate V_sh
            GR_log = np.array(self.las_data['GR'])
            GR_min = np.percentile(GR_log, 8.45)
            GR_max = np.percentile(GR_log, 94.9)
            V_sh = (GR_log - GR_min) / (GR_max - GR_min)
            V_sh = np.clip(V_sh, 0, 1)
            
            # Calculate S_w
            R_w = 0.05
            a = 1
            m = 2
            n=2
            total_porosity = np.random.uniform(0.1, 0.3, len(GR_log))  # Example total porosity
            R_t = np.array(self.las_data.RT)
            S_w = np.power((a * R_w / (np.power(total_porosity, m) *self.las_data['RT'])), 1/n)
            S_w = np.clip(S_w, 0, 1)

            # Effective Porosity
            Phi_eff = total_porosity * (1 - V_sh)
            
            # Add calculated columns to DataFrame
            self.las_data['V_sh'] = V_sh
            self.las_data['S_w'] = S_w
            self.las_data['Phi_eff'] = Phi_eff

            # Determine Reservoir Flag and Net Pay
            self.las_data['Reservoir_Flag'] = np.where(
                (self.las_data['V_sh'] < vsh_th) & (self.las_data['S_w'] < sw_th),
                1, 0
            )
            self.las_data['Net_Pay'] = np.where(
                (self.las_data['V_sh'] < vsh_th) &
                (self.las_data['S_w'] < sw_th) &
                (self.las_data['Phi_eff'] >= phi_eff_th),
                1, 0
            )

            # Filter Depth Range
            if min_depth is not None:
                self.las_Data = self.las_data[self.las_data['DEPTH'] >= min_depth]
            if max_depth is not None:
                self.las_data = self.las_data[self.las_data['DEPTH'] <= max_depth]

            # Plot All Subplots (Vertical Layout)
            depth = self.las_data['DEPTH']
            #self.figure.clear()
            #############################################PLot#############
             # Plot Gamma Ray and Vshale side by side (horizontally)
            fig, (ax1, ax2,ax3,ax4,ax5) = plt.subplots(figsize=(1, 2), nrows=1, ncols=5)
        
            # Gamma Ray plot (on the first track/left side)
            ax1.plot(self.las_data['V_sh'], depth, color='blue')
            ax1.set_xlabel("V_sh")
            ax1.set_ylabel("Depth")
            ax1.set_xlim(0, 1)  # Set the x-axis limit for Gamma Ray plot
            ax1.xaxis.set_label_position('top')  # Move the x-axis labels to the top
            ax1.invert_yaxis()  # Depth increases downward
            ax1.legend()
            ax1.grid(True)
        
        
            # SW Plot
            ax2.plot(self.las_data['S_w'], depth, color='red')
            ax2.set_xlabel("Sw")
            ax2.set_ylabel("Depth")
            ax2.xaxis.set_label_position('top')
            ax2.invert_yaxis()  # Depth increases downward
            ax2.legend()
            ax2.grid(True)
            
       #    Effective Porosity
            # Effective Porosity Plot
            ax3.plot(self.las_data['Phi_eff'], depth, color='purple')
            ax3.set_xlabel("Effective Porosity")
            ax3.set_ylabel("Depth")
            ax3.xaxis.set_label_position('top')
            ax3.invert_yaxis()  # Depth increases downward
            ax3.grid(True)
    
            #plt.tight_layout()
            # Reservoir Flag Plot
            ax4.plot(self.las_data['Reservoir_Flag'], depth, color='orange', label='Reservoir Flag', linestyle='-', linewidth=2)
            ax4.set_xlabel("Reservoir Flag")
            ax4.set_ylabel("Depth")
            ax4.xaxis.set_label_position('top')

            ax4.invert_yaxis()  # Depth increases downward
            ax4.legend()
            ax4.grid(True)
            
            # Net Pay Plot
            ax5.fill_betweenx(depth, self.las_data['Net_Pay'], color='green', step='mid', alpha=0.5)  # Added transparency
            ax5.set_xlabel("Net Pay")
            ax5.set_ylabel("Depth")
            ax5.xaxis.set_label_position('top')
            ax5.invert_yaxis()  # Depth increases downward
            ax5.grid(True)
            
              

            # Set the canvas to display the figure
            reservoir_ntg_canvas = FigureCanvas(fig)
            navi = NavigationToolbar2QT(reservoir_ntg_canvas, self.formation_evaluation_tab)
            
            container = QWidget()
            vlayout = QVBoxLayout(container)
            vlayout.addWidget(navi)
            vlayout.addWidget(reservoir_ntg_canvas)
        
            # Set the container widget in the QScrollArea
            self.formationGUI_ui.watersatplot_2.setWidget(container)
    
            plt.tight_layout()
        except ValueError as e:
            # Handle the case where conversion fails
            QMessageBox.warning(self, "Input Error", f"Invalid numerical input: {e}")
        except KeyError as e:
            QMessageBox.warning(self, "Data Error", f"Missing key in LAS data: {e}")
########################


        

##################################################
##################################################
##############################
    
##################Plot of histogram#########
    def plot_histogram(self):
        # Create a dialog to select log and color
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Log and Color for Histogram")
        layout = QHBoxLayout()

    # Combo box for selecting the log
        log_combo = QComboBox(dialog)
        log_combo.addItems(self.las_data.columns.tolist())
        layout.addWidget(QLabel("Select Log:"))
        layout.addWidget(log_combo)

    # Button to choose color
        color_button = QPushButton("Select Color", dialog)
        selected_color = None  # Variable to store the selected color

        def open_color_dialog():
            nonlocal selected_color  # Use nonlocal to modify the variable from the inner function
            color = QColorDialog.getColor()
            if color.isValid():
                selected_color = color.name()  # Get the selected color as a string
                color_button.setStyleSheet(f"background-color: {selected_color};color:white;")  # Update button color

        color_button.clicked.connect(open_color_dialog)
        layout.addWidget(color_button)

    # Add OK and Cancel buttons
        ok_button = QPushButton("OK", dialog)
        cancel_button = QPushButton("Cancel", dialog)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)

    # Connect the OK button to close the dialog and plot the histogram
        def on_ok():
            if selected_color: 
                # Only proceed if a color has been selected
                selected_log = log_combo.currentText()
                data = self.las_data[selected_log].dropna()  # Drop NaN values for cleaner plot
                self.canvas.figure.clf()  # Clear the previous plot
                ax = self.canvas.figure.add_subplot(111)

            # Use the selected color in the plot
                sns.histplot(data, bins=30, ax=ax, kde=True, color=selected_color)  # Add KDE for smooth distribution
                ax.set_title(f'Histogram of {selected_log}')
                ax.set_xlabel(selected_log)
                ax.set_ylabel('Counts')
                self.canvas.draw()  # Redraw the canvas
                dialog.accept()  # Close the dialog

        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(dialog.reject)

    # Execute the dialog and check if accepted
        if dialog.exec_() == QDialog.Accepted:
            # Handle any further actions if needed after dialog is closed
            pass
###########################
    def plot_scatter(self):
        # Plot a scatter plot for two selected logs
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Logs and Color Map for Scatter Plot")
        layout = QHBoxLayout()
        #Combo box
        log_x_combo=QComboBox(dialog)
        
        if hasattr(self, 'las_data'):
            dialog=QDialog(self)
            dialog.setWindowTitle("Select Logs and color map for scatter plot")
            layout=QHBoxLayout()
            # Combo box for selecting the X log
            log_x_combo = QComboBox(dialog)
            log_x_combo.addItems(self.las_data.columns.tolist())
            layout.addWidget(QLabel("Select X-axis :"))
            layout.addWidget(log_x_combo)

        # Combo box for selecting the Y log
            log_y_combo = QComboBox(dialog)
            log_y_combo.addItems(self.las_data.columns.tolist())
            layout.addWidget(QLabel("Select Y-axis:"))
            layout.addWidget(log_y_combo)

        # Combo box for selecting the color map
            colormap_combo = QComboBox(dialog)
            colormap_combo.addItems(plt.colormaps())
            layout.addWidget(QLabel("Select Color Map:"))
            layout.addWidget(colormap_combo)
            # Add OK and Cancel buttons
            button_layout = QHBoxLayout()
            ok_button = QPushButton("OK", dialog)
            cancel_button = QPushButton("Cancel", dialog)
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

            dialog.setLayout(layout)

#Connect the ok button
        def on_ok():
            selected_log_x = log_x_combo.currentText()
            selected_log_y = log_y_combo.currentText()
            selected_colormap = colormap_combo.currentText()

            x_data = self.las_data[selected_log_x].dropna()
            y_data = self.las_data[selected_log_y].dropna()
            plt_data = pd.concat([x_data, y_data], axis=1).dropna()  # Combine and drop NaN

            self.canvas.figure.clf()  # Clear the previous plot
            ax = self.canvas.figure.add_subplot(111)
            scatter = ax.scatter(plt_data[selected_log_x], plt_data[selected_log_y], c=plt_data[selected_log_y], cmap=selected_colormap, alpha=0.5)
            ax.set_title(f'Scatter Plot: {selected_log_x} vs {selected_log_y}')
            ax.set_xlabel(selected_log_x)
            ax.set_ylabel(selected_log_y)
            self.canvas.figure.colorbar(scatter, ax=ax, label=selected_log_y)
            self.canvas.draw()  # Redraw the canvas
            dialog.accept()  #
        
        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(dialog.reject)
        if dialog.exec_() == QDialog.Accepted:
            pass
        
            
###########################################################################################

############################################################################
    def plot_cross(self):
        # Unified dialog for cross plot selection
        if hasattr(self, 'las_data'):
            dialog = QDialog(self)
            dialog.setWindowTitle("Select Logs for Cross Plot")
            layout = QHBoxLayout(dialog)

        # X-axis Log selection
            log_1_combo = QComboBox(dialog)
            log_1_combo.addItems(self.las_data.columns.tolist())
            layout.addWidget(QLabel("Select X-axis Log:"))
            layout.addWidget(log_1_combo)

        # Y-axis Logs selection
            log_2_combo = QComboBox(dialog)
            log_2_combo.addItems(self.las_data.columns.tolist())
            layout.addWidget(QLabel("Select Y-axis Log 1:"))
            layout.addWidget(log_2_combo)

        # OK and Cancel buttons
            button_layout = QHBoxLayout()
            ok_button = QPushButton("OK", dialog)
            cancel_button = QPushButton("Cancel", dialog)
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

        # Handle OK button action
            def on_ok():
                log_1 = log_1_combo.currentText()
                log_2 = log_2_combo.currentText()
            # Ensure all selected logs have data
                if any(self.las_data[col].dropna().empty for col in [log_1, log_2]):
                    QMessageBox.warning(self, "Warning", "Selected logs have insufficient data.")
                    dialog.reject()
                else:
                    self.create_cross_plot(log_1, log_2)
                    dialog.accept()

            ok_button.clicked.connect(on_ok)
            cancel_button.clicked.connect(dialog.reject)

            dialog.exec_()

    def create_cross_plot(self, log_1, log_2):
        x_data = self.las_data[log_1].dropna()
        y_data = self.las_data[log_2].dropna()
    # Data validation and plotting
        plt_data = pd.concat([x_data, y_data], axis=1).dropna()
        if not plt_data.empty:
            self.canvas.figure.clf()
            ax= self.canvas.figure.add_subplot(111)
            ax.scatter(plt_data[log_1], plt_data[log_2], color='blue', alpha=0.5)
            ax.set_title(f'Cross Plot: {log_1} vs {log_2}')
            ax.set_xlabel(log_1)
            ax.set_ylabel(log_2)
            self.canvas.draw()
        else:
            QMessageBox.warning(self, "Warning", "Selected logs have insufficient data.")
#############################################################################################################
 #   ###
 #   ###
 #   #######                    
##########Code for triple combo plot########
 #   def plot_triple_combo(self):
 #       """Allow the user to select multiple logs and plot multiple triple combo plots dynamically."""
 #       if hasattr(self,'las_data'):
 #           dialog=QDialog(self)
 #           dialog.setWindowTitle("Select Logs for Triple Combo Plot")
 #           layout=QHBoxLayout(dialog)
 #           # Create a list to store the selected logs
 #           available_logs = self.las_data.columns.tolist()
 #           log_checkbox={}
 #           for log in available_logs:
 #               checkbox=QCheckBox(log)
 #               layout.addWidget(checkbox)
 #               log_checkbox[log]=checkbox
 #           # Depth column selection
 #           depth_combo = QComboBox(dialog)
 #           depth_combo.addItems(self.las_data.columns.tolist())
 #           layout.addWidget(QLabel("Select Depth Column:"))
 #           layout.addWidget(depth_combo)
 #       # OK and Cancel buttons
 #           button_layout = QHBoxLayout()
 #           ok_button = QPushButton("OK", dialog)
 #           cancel_button = QPushButton("Cancel", dialog)
 #           button_layout.addWidget(ok_button)
 #           button_layout.addWidget(cancel_button)
 #           layout.addLayout(button_layout)
 #           
 #           # Save button
 #           save_button = QPushButton("Save Plot", dialog)
 #           button_layout.addWidget(save_button)
 #           
 #           def on_ok():
 #               #Retrive the selected log and depth col
 #               selected_logs=[log for log, cb in log_checkbox.items() if cb.isChecked()]
 #               depth=depth_combo.currentText()
 #               
 #               if len(selected_logs)<3:
 #                   QMessageBox.warning(self, "Warning", "Select at least three logs to create a triple combo plot.")
 #                   return   
## Call the plot creation function with selected logs and depth
 #               self.create_multiple_triple_combo_plots(selected_logs, depth)
 #               dialog.accept()
 #               
 #           ok_button.clicked.connect(on_ok)
 #           cancel_button.clicked.connect(dialog.reject)
 #           dialog.exec_()   
 #   def create_multiple_triple_combo_plots(self,selected_logs,depth):
 #       log_groups = [selected_logs[i:i+3] for i in range(0, len(selected_logs), 3)]
 #       num_plots = len(log_groups)
 #       fig, axes = plt.subplots(num_plots, 3, figsize=(5, 10 * num_plots), sharey=True, squeeze=False)
 #       fig.subplots_adjust(hspace=0.3)
#
 #   # Generate each triple combo plot
 #       for i, log_group in enumerate(log_groups):
 #           if len(log_group) < 3:
 #               QMessageBox.warning(self, "Warning", f"Only {len(log_group)} logs selected for the last plot. Please select logs in multiples of three.")
 #               continue
 #           ax1,ax2,ax3=axes[i,:]
 #           data=self.las_data[[*log_group,depth]].dropna()
 #           if data.empty:
 #               QMessageBox.warning(self, "Error", f"Selected logs {log_group} have insufficient data.")
 #               continue
 #           # Condition for applying the Sand Line and Shale Line
 #           if 'GR' in log_group:
 #               gr_index = log_group.index('GR')
 #               p_5 = data['GR'].quantile(0.05)
 #               p_95 = data['GR'].quantile(0.95)
 #               # Plot first log (e.g., gamma ray)
 #               axes[i, gr_index].axvline(x=p_5, label='Sand Line', color='blue', linestyle='--', linewidth=1)
 #               axes[i, gr_index].axvline(x=p_95, label='Shale Line', color='green', linestyle='--', linewidth=1)
#
 #           # Plot first log 
 #           ax1.plot(data[log_group[0]], data[depth], color='red', label=log_group[0], linewidth=1)
 #           ax1.set_xlabel(log_group[0], color='black', size=11)
 #           ax1.legend(loc='upper right')
 #           ax1.grid(True)
#
 #       # Plot second log
 #           ax2.plot(data[log_group[1]], data[depth], color='black', label=log_group[1], linewidth=1)
 #           ax2.set_xlabel(log_group[1], color='black', size=11)
 #           ax2.legend(loc='upper right')
 #           ax2.grid(True)
#
 #       # Plot third log 
 #           ax3.plot(data[log_group[2]], data[depth], color='blue', label=log_group[2], linewidth=1)
 #           ax3.set_xlabel(log_group[2], color='blue', size=11)
 #           ax3.legend(loc='upper right')
 #           ax3.grid(True)
 #           # Adjust depth axis (shared across all plots)
 #           for ax in (ax1,ax2,ax3):
 #               ax.set_ylim(data[depth].max(), data[depth].min())  # Depth increases downward
 #               #ax.invert_yaxis()
 #               ax.xaxis.set_ticks_position('top')
 #               ax.xaxis.set_label_position('top')
 #               ax.spines.top.set_position(('axes', 1.01))
 #               ax.set_ylabel('Depth (m)', size=12)
 #               ax.legend()
 #               ax.grid(True)    
 #       fig.suptitle('Triple Combo Plots', fontsize=12, fontweight='bold', bbox=dict(facecolor='skyblue', edgecolor='black', boxstyle='round,pad=0.3'),y=0.98)
 #       plt.tight_layout()
 #       # Display the plot(s) in the application
 #       self.canvas.figure = fig
 #       self.canvas.draw()            
 #       
 #       #Saving the plots
 #       self.canvas.figure = fig
 #       self.canvas.draw()
 #       
 #   def show_save_dialog(self, fig):
 #       """Open a file dialog to save the plot."""
 #       options = QFileDialog.Options()
 #       filename, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
 #       if filename:
 #           fig.savefig(filename, dpi=300)  # Save the figure with high resolution
 #           QMessageBox.information(self, "Success", f"Plot saved as {filename}")
 #       
########################PLOT FORMATION TOP CODE#################
    def plot_formation_top(self):
        """plot for formation top"""
        if hasattr(self,'las_data'):
            #Prompt the user to select the logs for depth
            depth_log, ok_depth = QInputDialog.getItem(self, "Select Depth Log for Formation Top Plot", "Depth log:", self.las_data.columns.tolist(), 0, False)
            if not ok_depth:
                return
            #Prompt the user to select the logs for formation top
            formation_log, ok_formation = QInputDialog.getItem(self, "Select Formation Top Log for Formation Top Plot", "Formation Top log:", self.las_data.columns.tolist(), 0, False)
            if not ok_formation:
                return
            depth_data=self.las_data[depth_log].dropna()
            formation_data=self.las_data[formation_log].dropna()
            #drop nun value
            plot_data=pd.concat([depth_data,formation_data],axis=1).dropna()
            #clear the previous plot and create a new formation plot
            self.canvas.figure.clf()
            ax=self.canvas.figure.add_subplot(111)
            ax.plot(plot_data[formation_log],plot_data[depth_log],color='red',lw=2)
            ax.set_title(f'Formation Top Plot: {formation_log} vs {depth_log}') 
            ax.set_xlabel(formation_log)
            ax.set_ylabel(depth_log)
            ax.invert_yaxis()  #####It means depth increases downward
            ax.grid(True)
            self.canvas.draw()




############################################################################################
#############################################################################################
    




#################################################################################################
########################################################################################
################################################################Taskbar details################
# Add the splash screen setup in the main function
def main():
    app = QApplication(sys.argv)
    
    # Splash Screen Setup
    splash_pix = QPixmap("/home/ashraf/Desktop/Designer.jpeg")  # Replace with the path to your splash image
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.FramelessWindowHint)  # Frameless look for the splash
    splash.show()
    
    # Simulate a loading delay
    QTimer.singleShot(1000, splash.close)  # Show the splash for 3 seconds
    
    # Create the main window
    main_window = PetroAnalysis()
    QTimer.singleShot(1000, main_window.show)  # Show the main window after the splash

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
