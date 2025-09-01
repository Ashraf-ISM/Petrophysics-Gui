import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QSlider, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFormLayout, QTabWidget, QGroupBox, QSpinBox, QTextEdit, QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy as np
import plotly.graph_objects as go
from PyQt5.QtWebEngineWidgets import QWebEngineView

class CoreFunctionality(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Petrophysics Analysis Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set up main layout
        self.layout = QVBoxLayout(self)
        
        # Instruction label
        instruction_label = QLabel("Enter petrophysical parameters below and click 'Calculate' for results or 'Plot' to see analysis.")
        instruction_label.setFont(QFont('Arial', 10))
        instruction_label.setStyleSheet("color: #333;")
        self.layout.addWidget(instruction_label)

        # Tabs setup
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Core functionality tab
        self.core_functionality_tab = QWidget()
        self.tabs.addTab(self.core_functionality_tab, "Core Functionality")
        self.create_core_functionality_tab()

    def create_core_functionality_tab(self):
        # Main grid layout for organizing the sections
        layout = QGridLayout()
        
        # **Input Section: Petrophysical Parameters**
        input_group = QGroupBox("Input: Petrophysical Parameters")
        input_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 12pt; color: #2E8B57; }")
        input_form_layout = QFormLayout()
        
        # Input fields with placeholders for example values
        self.porosity_input = QLineEdit()
        self.porosity_input.setPlaceholderText("e.g., 25")
        self.porosity_input.setToolTip("Enter Porosity (phi) in percentage (e.g., 25)")
        
        self.Formation_Water_Resistivity_input = QLineEdit()
        self.Formation_Water_Resistivity_input.setPlaceholderText("e.g., 0.1")
        self.Formation_Water_Resistivity_input.setToolTip("Enter the Formation Water Resistivity (R_w) (e.g., 0.1)")
        
        self.Formation_Resistivity_input = QLineEdit()
        self.Formation_Resistivity_input.setPlaceholderText("e.g., 20")
        self.Formation_Resistivity_input.setToolTip("Enter Formation Resistivity (R_t) (e.g., 20)")
        
        self.water_saturation_input = QLineEdit()
        self.water_saturation_input.setPlaceholderText("e.g., 30")
        self.water_saturation_input.setToolTip("Enter Water Saturation in percentage (e.g., 30)")

        # Adding input fields to the form layout
        input_form_layout.addRow("Porosity (%):", self.porosity_input)
        input_form_layout.addRow("Formation Water Resistivity:", self.Formation_Water_Resistivity_input)
        input_form_layout.addRow("Formation_Resistivity:", self.Formation_Resistivity_input)
        input_form_layout.addRow("Water Saturation (%):", self.water_saturation_input)
        input_group.setLayout(input_form_layout)
        
        # Sensitivity Analysis Section
        sliders_group = QGroupBox("Sensitivity Analysis")
        sliders_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 12pt; color: #2E8B57; }")
        sliders_layout = QVBoxLayout()
        
        # Sliders for the Variables of a, m and n
        self.saturation_exponent_slider = self.create_custom_slider("Saturation Exponent (n)", 1.8, 4.0, 2.0)
        self.tortuosity_factor_slider = self.create_custom_slider("Tortuosity Factor (a)", 0.62, 1.0, 0.8)
        self.cementation_factor_slider = self.create_custom_slider("Cementation Factor (m)", 1.7, 3.0, 2.0)
        
        sliders_layout.addWidget(self.saturation_exponent_slider)
        sliders_layout.addWidget(self.tortuosity_factor_slider)
        sliders_layout.addWidget(self.cementation_factor_slider)
        sliders_group.setLayout(sliders_layout)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton("Calculate Properties")
        self.plot_button = QPushButton("Plot Sensitivity Analysis")
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.plot_button)
        
        # Connect buttons to functions
        self.calculate_button.clicked.connect(self.calculate_petrophysical_properties)
        self.plot_button.clicked.connect(self.plot_sensitivity_analysis)
        
        # **Results Display**
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFixedHeight(100) 
        self.result_display.setFont(QFont('Arial', 10))
        self.result_display.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ccc;")
        self.result_display.setText("Results will be displayed here after calculation.")
        
        # **Plot Display Panel**
        self.plot_view = QWebEngineView()
        
        # Organizing components into the layout
        layout.addWidget(input_group, 0, 0, 1, 2)
        layout.addWidget(sliders_group, 1, 0, 1, 2)
        layout.addWidget(self.plot_view, 0, 2, 2, 1)
        layout.addLayout(button_layout, 2, 0, 1, 3)
        layout.addWidget(self.result_display, 3, 0, 1, 3)  
        
        # Set layout to the core functionality tab
        self.core_functionality_tab.setLayout(layout)

    def create_custom_slider(self, label_text, min_value, max_value, default_value):
        # Custom slider widget with label and spinbox
        slider_widget = QWidget()
        slider_layout = QHBoxLayout()
        
        label = QLabel(label_text)
        label.setFont(QFont('Arial', 10))
        
        # Scale the values to integers (multiplying by 100 for 2 decimal precision)
        int_min = int(min_value * 100)
        int_max = int(max_value * 100)
        int_default = int(default_value * 100)
        
        # Create the slider with integer values
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(int_min)
        slider.setMaximum(int_max)
        slider.setValue(int_default)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        
        # Use QDoubleSpinBox for floating-point numbers
        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(default_value)
        spinbox.setSingleStep(0.01)  
        
        # Synchronize slider and spinbox
        slider.valueChanged.connect(lambda value: spinbox.setValue(value / 100.0))  # Convert to float for display
        spinbox.valueChanged.connect(lambda value: slider.setValue(int(value * 100)))  # Convert to integer for slider
        
        slider_layout.addWidget(label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(spinbox)
        
        slider_widget.setLayout(slider_layout)
        return slider_widget

    def calculate_petrophysical_properties(self):
        try:
            # Retrieve values from input fields
            porosity = float(self.porosity_input.text())
            Formation_Water_Resistivity = float(self.Formation_Water_Resistivity_input.text())
            Formation_Resistivity = float(self.Formation_Resistivity_input.text())
            # Gather the values of the sliders
            tortuosity_factor = self.tortuosity_factor_slider.findChild(QDoubleSpinBox).value()
            cementation_factor = self.cementation_factor_slider.findChild(QDoubleSpinBox).value()
            saturation_exponent = self.saturation_exponent_slider.findChild(QDoubleSpinBox).value()

            # Archie's Equation for Water Saturation (Sw)
            water_saturation = ((tortuosity_factor * Formation_Water_Resistivity) /
                                (Formation_Resistivity * porosity**cementation_factor)) ** (1 / saturation_exponent)
            effective_porosity = porosity * 100  # Optional: calculated from other parameters if needed
            
            result_text = f"Water Saturation (Sw): {water_saturation:.2f} (fraction)\nEffective Porosity: {effective_porosity:.2f} %"
            self.result_display.setText(result_text)

        except ValueError:
            # Error message for invalid input
            self.result_display.setText("Error: Please enter valid numbers.")

    def plot_sensitivity_analysis(self):
        # Example plot for sensitivity analysis
        porosity_range = np.linspace(5, 30, 100)
        resistivity = 0.62 * porosity_range ** -1.5

        # Creating the Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=porosity_range, y=resistivity, mode='lines', name="Resistivity vs. Porosity"))
        fig.update_layout(
            title="Parameter Sensitivity Analysis",
            xaxis_title="Porosity (%)",
            yaxis_title="Resistivity (Ω·m)"
        )

        # Render plot in the QWebEngineView
        html = fig.to_html(include_plotlyjs="cdn")
        self.plot_view.setHtml(html)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoreFunctionality()
    window.show()
    sys.exit(app.exec_())
