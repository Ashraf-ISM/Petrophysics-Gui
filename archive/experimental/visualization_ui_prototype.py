from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 850)
        Form.setWindowTitle("Advanced Visualization Tool")
        Form.setStyleSheet("background-color: #f0f8ff; font-family: Arial;")
        
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #c0c0c0; }
            QTabBar::tab { background: #e6e6fa; padding: 10px; margin: 2px; border-radius: 5px; }
            QTabBar::tab:selected { background: #add8e6; }
        """)
        self.tabWidget.setObjectName("tabWidget")
        
        # Tab 1 - Visualization and Histogram
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setMinimumSize(QtCore.QSize(250, 200))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setStyleSheet("background-color: #ffffff; border: 1px solid #d3d3d3; border-radius: 10px;")
        self.frame.setObjectName("frame")
        
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setText("Select Data Set:")
        self.label.setStyleSheet("font-weight: bold;")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setStyleSheet("padding: 5px;")
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 2)
        
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setText("Bin size:")
        self.label_2.setStyleSheet("font-weight: bold;")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        
        self.spinBox = QtWidgets.QSpinBox(self.frame)
        self.spinBox.setStyleSheet("padding: 5px;")
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 1, 2, 1, 2)
        
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setText("Set Color:")
        self.label_3.setStyleSheet("font-weight: bold;")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        
        self.colorButton = QtWidgets.QPushButton(self.frame)
        self.colorButton.setText("Choose Color")
        self.colorButton.setStyleSheet("padding: 5px; background-color: #add8e6; border-radius: 5px;")
        self.colorButton.setObjectName("colorButton")
        self.gridLayout.addWidget(self.colorButton, 2, 2, 1, 2)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setText("Apply Changes")
        self.pushButton_2.setStyleSheet("padding: 10px; background-color: #32cd32; color: white; border-radius: 5px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 0, 1, 4)
        
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)
        
        self.scrollArea = QtWidgets.QScrollArea(self.tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("border: 1px solid #d3d3d3;")
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 900, 700))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 1, 2, 1)
        
        self.tabWidget.addTab(self.tab, "Histogram")

        
        # Tab 2 - Cross Plot and Custom Graph
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setStyleSheet("background-color: #ffffff; border: 1px solid #d3d3d3; border-radius: 10px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setText("X Axis:")
        self.label_4.setStyleSheet("font-weight: bold;")
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        
        self.xcrosscomboBox = QtWidgets.QComboBox(self.frame_2)
        self.xcrosscomboBox.setStyleSheet("padding: 5px;")
        self.xcrosscomboBox.setObjectName("xcrosscomboBox")
        self.gridLayout_4.addWidget(self.xcrosscomboBox, 0, 1, 1, 2)
        
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setText("Y Axis:")
        self.label_5.setStyleSheet("font-weight: bold;")
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        
        self.ycrosscomboBox = QtWidgets.QComboBox(self.frame_2)
        self.ycrosscomboBox.setStyleSheet("padding: 5px;")
        self.ycrosscomboBox.setObjectName("ycrosscomboBox")
        self.gridLayout_4.addWidget(self.ycrosscomboBox, 1, 1, 1, 2)
        
        self.pushButtoncross = QtWidgets.QPushButton(self.frame_2)
        self.pushButtoncross.setText("Generate Plot")
        self.pushButtoncross.setStyleSheet("padding: 10px; background-color: #4682b4; color: white; border-radius: 5px;")
        self.pushButtoncross.setObjectName("pushButtoncross")
        self.gridLayout_4.addWidget(self.pushButtoncross, 3, 0, 1, 3)
        
        self.gridLayout_5.addWidget(self.frame_2, 0, 0, 1, 1)
        
        self.crossscrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.crossscrollArea.setWidgetResizable(True)
        self.crossscrollArea.setStyleSheet("border: 1px solid #d3d3d3;")
        self.crossscrollArea.setObjectName("crossscrollArea")
        
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 950, 700))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.crossscrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_5.addWidget(self.crossscrollArea, 0, 1, 2, 1)
        
        self.tabWidget.addTab(self.tab_2, "Cross Plot and Custom Graph")
        
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)


# The following part is required to run the application:

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
