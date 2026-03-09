import logging

from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QDockWidget,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QTextBrowser,
    QToolBar,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QStyle,
    QComboBox,   # ← ADD THIS
)
from PyQt5.QtCore import QSize, Qt

from ..features.petro_analysis import PetroAnalysis



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.petro_analysis_widget = PetroAnalysis()

        workspace = QWidget()
        workspace.setObjectName("workspaceShell")
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(12, 12, 12, 12)
        workspace_layout.addWidget(self.petro_analysis_widget)
        self.setCentralWidget(workspace)

        self.setWindowTitle("PetroAnalysis Studio")
        self.resize(1480, 920)
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().showMessage("Workspace ready")

        self.create_menu_bar()
        self.create_toolbar()
        self.create_workspace_dock()
        self.apply_main_window_style()
        self.petro_analysis_widget.workspace_changed.connect(self._sync_workspace_tree)
        self.petro_analysis_widget.file_context_changed.connect(self._update_command_file_label)
        self._update_command_file_label("No active file")
        self._sync_workspace_tree(self.petro_analysis_widget.current_workspace_key)

    def apply_main_window_style(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background: #dfe6ee;
            }
            QMenuBar {
                background: #1f2630;
                border: none;
                color: #eef4fb;
                padding-left: 8px;
            }
            QMenuBar::item {
                padding: 8px 12px;
                margin: 0 2px;
                background: transparent;
                border-top: 3px solid transparent;
            }
            QMenuBar::item:selected {
                background: #2c3644;
                border-top-color: #f4b657;
                color: #ffffff;
            }
            QMenu {
                background: #ffffff;
                border: 1px solid #cad4df;
                color: #203042;
            }
            QMenu::item {
                padding: 5px 24px 5px 22px;
            }
            QMenu::item:selected {
                background: #edf4fb;
                color: #1a4066;
            }
            QToolBar#commandBar {
                background: #f4f7fb;
                border: none;
                border-bottom: 1px solid #c9d3df;
                spacing: 6px;
                padding: 4px 8px;
            }
            QToolButton#commandButton {
                background: #ffffff;
                color: #243447;
                border: 1px solid #d4dde8;
                border-radius: 9px;
                padding: 6px 10px;
                min-height: 24px;
                font-weight: 700;
            }
            QToolButton#commandButton:hover {
                background: #eef5fc;
                border-color: #c7d8ea;
            }
            QToolButton#commandButton:pressed {
                background: #e1edf8;
            }
            QLabel#commandMeta {
                color: #66788c;
                font-size: 11px;
                font-weight: 700;
            }
            QLabel#commandFileLabel {
                background: #ffffff;
                color: #2d4b67;
                border: 1px solid #cbd9e7;
                border-radius: 9px;
                padding: 6px 10px;
                font-size: 11px;
                font-weight: 700;
            }
            QComboBox#commandPagePicker {
                background: #ffffff;
                color: #243447;
                border: 1px solid #cbd9e7;
                border-radius: 9px;
                padding: 4px 8px;
                min-width: 210px;
            }
            QLabel#commandHint {
                color: #4e5d6f;
                font-size: 11px;
                font-weight: 600;
            }
            QWidget#workspaceShell {
                background: #e8eef5;
            }
            QDockWidget#projectExplorerDock {
                color: #f7fbff;
                font-weight: 700;
            }
            QDockWidget#projectExplorerDock::title {
                background: #1f2630;
                color: #f7fbff;
                padding: 9px 12px;
                text-align: left;
            }
            QWidget#dockPanel {
                background: #f8fbff;
                border-right: 1px solid #ced8e4;
            }
            QLabel#dockPanelTitle {
                color: #223248;
                font-size: 14px;
                font-weight: 700;
            }
            QLabel#dockPanelSubtitle, QLabel#dockFooter {
                color: #617286;
                font-size: 11px;
            }
            QTreeWidget#workspaceTree {
                background: #ffffff;
                border: 1px solid #d4dde8;
                border-radius: 10px;
                padding: 6px;
                color: #27384d;
                alternate-background-color: #f5f9fd;
            }
            QTreeView#workspaceTree::item {
                padding: 6px 8px;
                border-radius: 6px;
            }
            QTreeView#workspaceTree::item:selected {
                background: #e7f1fb;
                color: #1a436c;
            }
            QMainWindow::separator {
                background: #cfd7e0;
                width: 1px;
                height: 1px;
            }
            QStatusBar {
                background: #f7f9fc;
                border-top: 1px solid #cad3de;
                color: #26384d;
            }
            """
        )

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        self._add_action(file_menu, "Export as CSV", self.export_csv)
        self._add_action(file_menu, "Export Plot as PNG", lambda: self.export_plot("png"))
        self._add_action(file_menu, "Export Plot as PDF", lambda: self.export_plot("pdf"))
        file_menu.addSeparator()
        self._add_action(file_menu, "E&xit", self.close)

        well_menu = menu_bar.addMenu("&Well")
        self._add_placeholder_action(well_menu, "Well Header")
        self._add_placeholder_action(well_menu, "Well Manager")

        io_menu = menu_bar.addMenu("&Input / Output")
        self._add_placeholder_action(io_menu, "Import Logs")
        self._add_placeholder_action(io_menu, "Export Reports")

        edit_menu = menu_bar.addMenu("&Edit")
        self._add_placeholder_action(edit_menu, "Preferences")

        view_menu = menu_bar.addMenu("&View")
        self._add_placeholder_action(view_menu, "Refresh Workspace")

        workspace_menu = menu_bar.addMenu("&Workspace")
        self._add_action(workspace_menu, "Data Loading", self._open_data_loading)
        self._add_action(workspace_menu, "Well Data and Stats", self._open_data_preview)
        self._add_action(workspace_menu, "Basic Visualization", self._open_visualization)
        self._add_action(workspace_menu, "Formation Evaluation", self._open_formation)

        calc_menu = menu_bar.addMenu("&Calculation")
        self._add_placeholder_action(calc_menu, "Basic Log Functions")
        env_menu = calc_menu.addMenu("Environmental Corrections")
        self._add_placeholder_action(env_menu, "Schlumberger Corrections")
        self._add_placeholder_action(env_menu, "Halliburton Corrections")
        self._add_placeholder_action(env_menu, "Baker Atlas Corrections")

        interp_menu = menu_bar.addMenu("&Interpretation")
        self._add_placeholder_action(interp_menu, "Shale Volume")
        self._add_placeholder_action(interp_menu, "Water Saturation")

        tools_menu = menu_bar.addMenu("&Tools")
        self._add_placeholder_action(tools_menu, "Curve Aliasing")

        help_menu = menu_bar.addMenu("&Help")
        self._add_action(help_menu, "Help Topics", self.show_help)
        self._add_action(help_menu, "Help Center", self.show_help_center)
        help_menu.addSeparator()
        self._add_action(help_menu, "About", self.show_about)
        self._add_action(help_menu, "Motive", self.show_motive)

    def create_toolbar(self):
        toolbar = QToolBar("Workspace Commands", self)
        toolbar.setObjectName("commandBar")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        command_row = QWidget()
        command_row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        command_layout = QHBoxLayout(command_row)
        command_layout.setContentsMargins(6, 4, 6, 4)
        command_layout.setSpacing(8)

        command_layout.addWidget(self._create_command_button("Input", self.style().standardIcon(QStyle.SP_DirOpenIcon), self._open_data_loading))
        command_layout.addWidget(self._create_command_button("Well Data", self.style().standardIcon(QStyle.SP_FileDialogListView), self._open_data_preview))
        command_layout.addWidget(self._create_command_button("Visualization", self.style().standardIcon(QStyle.SP_FileDialogDetailedView), self._open_visualization))
        command_layout.addWidget(self._create_command_button("Formation", self.style().standardIcon(QStyle.SP_ComputerIcon), self._open_formation))
        command_layout.addSpacing(8)
        command_layout.addWidget(self._create_command_button("Export CSV", self.style().standardIcon(QStyle.SP_DialogSaveButton), self.export_csv))
        command_layout.addWidget(self._create_command_button("Export PNG", self.style().standardIcon(QStyle.SP_DesktopIcon), lambda: self.export_plot("png")))
        command_layout.addWidget(self._create_command_button("Help", self.style().standardIcon(QStyle.SP_MessageBoxInformation), self.show_help_center))
        command_layout.addStretch()

        goto_label = QLabel("Go to")
        goto_label.setObjectName("commandMeta")
        command_layout.addWidget(goto_label)

        self.command_page_picker = QComboBox()
        self.command_page_picker.setObjectName("commandPagePicker")
        self.command_page_picker.addItem("Data Loading", "data_loading")
        self.command_page_picker.addItem("Well Data and Stats", "well_data")
        self.command_page_picker.addItem("Basic Visualization", "visualization")
        self.command_page_picker.addItem("Formation Evaluation", "formation")
        self.command_page_picker.currentIndexChanged.connect(self._handle_command_page_change)
        command_layout.addWidget(self.command_page_picker)

        active_label = QLabel("Active file")
        active_label.setObjectName("commandMeta")
        command_layout.addWidget(active_label)

        self.command_file_label = QLabel("No active file")
        self.command_file_label.setObjectName("commandFileLabel")
        command_layout.addWidget(self.command_file_label)
        toolbar.addWidget(command_row)

    def _create_command_button(self, text, icon, callback):
        button = QToolButton()
        button.setObjectName("commandButton")
        button.setText(text)
        button.setIcon(icon)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.clicked.connect(callback)
        return button

    def create_workspace_dock(self):
        dock = QDockWidget("Input Navigator", self)
        dock.setObjectName("projectExplorerDock")
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        dock.setMinimumWidth(280)
        dock.setMaximumWidth(320)

        panel = QWidget()
        panel.setObjectName("dockPanel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        panel_layout.setSpacing(10)

        title = QLabel("Input Navigator")
        title.setObjectName("dockPanelTitle")
        subtitle = QLabel("Project objects, loaded assets, and interpretation lanes.")
        subtitle.setObjectName("dockPanelSubtitle")

        tree = QTreeWidget()
        tree.setObjectName("workspaceTree")
        tree.setHeaderHidden(True)
        tree.setAlternatingRowColors(True)
        tree.itemClicked.connect(self._handle_workspace_tree_click)
        self.workspace_tree = tree

        sections = {
            "Project Workspace": ["Data Loading", "Well Data Table", "Visualization", "Formation Evaluation"],
            "Loaded Inputs": ["Well Logs", "Formation Tops", "Core Data", "Curve Aliasing"],
            "Interpretation": ["VShale", "Porosity", "Water Saturation", "Exported Deliverables"],
        }

        for section_name, children in sections.items():
            parent = QTreeWidgetItem([section_name])
            for child_name in children:
                QTreeWidgetItem(parent, [child_name])
            tree.addTopLevelItem(parent)
            parent.setExpanded(True)

        footer = QLabel("Use the command bar or this navigator to switch workspace pages.")
        footer.setObjectName("dockFooter")
        footer.setWordWrap(True)

        panel_layout.addWidget(title)
        panel_layout.addWidget(subtitle)
        panel_layout.addWidget(tree, 1)
        panel_layout.addWidget(footer)

        dock.setWidget(panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def _add_action(self, menu, title, callback):
        action = QAction(title, self)
        action.triggered.connect(callback)
        menu.addAction(action)
        return action

    def _handle_command_page_change(self, index):
        if index < 0:
            return
        page_key = self.command_page_picker.itemData(index)
        if page_key == "data_loading":
            self._open_data_loading()
        elif page_key == "well_data":
            self._open_data_preview()
        elif page_key == "visualization":
            self._open_visualization()
        elif page_key == "formation":
            self._open_formation()

    def _add_placeholder_action(self, menu, title):
        self._add_action(menu, title, lambda checked=False, t=title: self._show_placeholder(t))

    def _show_placeholder(self, feature_name):
        self.statusBar().showMessage(f"{feature_name} menu ready for integration.", 3000)

    def _open_data_loading(self):
        if hasattr(self.petro_analysis_widget, "open_data_loading_page"):
            self.petro_analysis_widget.open_data_loading_page()

    def _open_data_preview(self):
        if hasattr(self.petro_analysis_widget, "open_data_preview"):
            self.petro_analysis_widget.open_data_preview()

    def _open_visualization(self):
        if hasattr(self.petro_analysis_widget, "open_visualization_page"):
            self.petro_analysis_widget.open_visualization_page()

    def _open_formation(self):
        if hasattr(self.petro_analysis_widget, "open_formation_evaluation_page"):
            self.petro_analysis_widget.open_formation_evaluation_page()

    def _handle_workspace_tree_click(self, item, column):
        del column
        if hasattr(self.petro_analysis_widget, "navigate_to_section"):
            self.petro_analysis_widget.navigate_to_section(item.text(0))

    def _sync_workspace_tree(self, page_key):
        if not hasattr(self, "workspace_tree"):
            return
        target_texts = {
            "data_loading": "Data Loading",
            "well_data": "Well Data Table",
            "visualization": "Visualization",
            "formation": "Formation Evaluation",
        }
        target_item = self._find_tree_item_by_text(target_texts.get(page_key, "Data Loading"))
        if target_item is not None:
            self.workspace_tree.blockSignals(True)
            self.workspace_tree.setCurrentItem(target_item)
            target_item.setExpanded(True)
            parent = target_item.parent()
            while parent is not None:
                parent.setExpanded(True)
                parent = parent.parent()
            self.workspace_tree.blockSignals(False)
        if hasattr(self, "command_page_picker"):
            index = self.command_page_picker.findData(page_key)
            if index >= 0:
                self.command_page_picker.blockSignals(True)
                self.command_page_picker.setCurrentIndex(index)
                self.command_page_picker.blockSignals(False)

    def _find_tree_item_by_text(self, text):
        if not hasattr(self, "workspace_tree"):
            return None
        for index in range(self.workspace_tree.topLevelItemCount()):
            match = self._find_tree_item_recursive(self.workspace_tree.topLevelItem(index), text)
            if match is not None:
                return match
        return None

    def _find_tree_item_recursive(self, item, text):
        if item.text(0) == text:
            return item
        for child_index in range(item.childCount()):
            match = self._find_tree_item_recursive(item.child(child_index), text)
            if match is not None:
                return match
        return None

    def _update_command_file_label(self, text):
        if hasattr(self, "command_file_label"):
            self.command_file_label.setText(text)

    def export_csv(self):
        current_widget = self.petro_analysis_widget
        if hasattr(current_widget, "las_data") and not current_widget.las_data.empty:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Results as CSV",
                "",
                "CSV Files (*.csv);;All Files (*)",
                options=options,
            )
            if file_path:
                try:
                    current_widget.las_data.to_csv(file_path, index=False)
                    QMessageBox.information(self, "Success", "Results exported successfully as CSV!")
                except Exception as exc:
                    QMessageBox.critical(self, "Error", f"Failed to export CSV: {exc}")
        else:
            QMessageBox.warning(self, "No Data", "No data available to export.")

    def export_plot(self, fmt="png"):
        current_widget = self.petro_analysis_widget
        if hasattr(current_widget, "evaluation_canvas"):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                f"Export Plot as {fmt.upper()}",
                "",
                f"{fmt.upper()} Files (*.{fmt});;All Files (*)",
                options=options,
            )
            if file_path:
                try:
                    logging.debug("Rendering the plot before saving.")
                    current_widget.evaluation_canvas.figure.canvas.draw()
                    current_widget.evaluation_canvas.figure.savefig(file_path, format=fmt)
                    QMessageBox.information(self, "Success", f"Plot exported successfully as {fmt.upper()}!")
                except Exception as exc:
                    logging.error("Error during plot export: %s", exc)
                    QMessageBox.critical(self, "Error", f"Failed to export plot: {exc}")
        else:
            QMessageBox.warning(self, "No Plot", "No plot available to export.")

    def show_help_center(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("PetroAnalysis Help")
        dialog.resize(980, 640)

        root_layout = QHBoxLayout(dialog)
        root_layout.setContentsMargins(6, 6, 6, 6)

        tree = QTreeWidget()
        tree.setHeaderLabels(["Contents"])
        tree.setMaximumWidth(280)

        sections = {
            "Introduction": "Overview of PetroAnalysis workspace and workflow.",
            "Data Loading": "Load LAS/CSV/TXT, inspect headers, and validate columns.",
            "Visualization": "Histogram, crossplot, and multi-track workflows.",
            "Formation Evaluation": "Vshale, porosity, saturation, and quality-control tools.",
            "Exporting": "Export tables and generated figures to files.",
        }

        for key in sections:
            item = QTreeWidgetItem([key])
            tree.addTopLevelItem(item)

        content = QTextBrowser()
        content.setHtml("<h2>Introduction</h2><p>Overview of PetroAnalysis workspace and workflow.</p>")

        def on_tree_change():
            selected = tree.currentItem()
            if not selected:
                return
            title = selected.text(0)
            body = sections.get(title, "")
            content.setHtml(f"<h2>{title}</h2><p>{body}</p>")

        tree.itemSelectionChanged.connect(on_tree_change)
        tree.setCurrentItem(tree.topLevelItem(0))

        root_layout.addWidget(tree)
        root_layout.addWidget(content, 1)
        dialog.exec_()

    def show_help(self):
        self.show_help_center()

    def show_about(self):
        QMessageBox.information(
            self,
            "About PetroAnalysis",
            "<html><h1>PetroAnalysis</h1><p>Petrophysical analysis and visualization desktop application.</p></html>",
        )

    def show_motive(self):
        QMessageBox.information(
            self,
            "Motive",
            "<html><h1>Motive</h1><p>Improve well-log interpretation workflows with an integrated workspace.</p></html>",
        )
