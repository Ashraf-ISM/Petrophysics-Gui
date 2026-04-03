#!/usr/bin/env python3
"""
PetroAnalyst Pro - Main Application Entry Point

Loads the Qt Designer UI file and wires up basic interactions for the
professional petrophysics analysis application.

Usage:
    python src/main.py

Requirements:
    PyQt5, lasio, dlisio, pandas, matplotlib, numpy
"""

import sys
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox,
    QTreeWidgetItem, QLabel, QProgressBar
)
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtGui import QFont

# ---------------------------------------------------------------------------
# Resolve the path to main_window.ui relative to this file
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
UI_FILE = os.path.join(_HERE, "main_window.ui")


class PetroAnalystMain(QMainWindow):
    """Main application window for PetroAnalyst Pro."""

    def __init__(self):
        super().__init__()
        # Load the Qt Designer UI file
        uic.loadUi(UI_FILE, self)

        # Status bar permanent widgets
        _sb = QtWidgets.QMainWindow.statusBar(self)
        self._status_label = QLabel("  Ready  ")
        self._status_label.setStyleSheet("color: #a0c8e8;")
        _sb.addPermanentWidget(self._status_label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setFixedWidth(180)
        self._progress_bar.setFixedHeight(14)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        _sb.addPermanentWidget(self._progress_bar)

        _sb.showMessage(
            "PetroAnalyst Pro  |  No project loaded  |  Ready"
        )

        self._connect_actions()
        self._populate_defaults()

    # ------------------------------------------------------------------
    # Signal / slot wiring
    # ------------------------------------------------------------------
    def _connect_actions(self):
        """Connect menu actions and button clicks to handlers."""
        # ---- File menu ----
        self._safe_connect("actionNewProject", "triggered", self._on_new_project)
        self._safe_connect("actionOpenProject", "triggered", self._on_open_project)
        self._safe_connect("actionSaveProject", "triggered", self._on_save_project)
        self._safe_connect("actionExit", "triggered", self.close)

        # ---- Well menu ----
        self._safe_connect("actionAddWell", "triggered", self._on_add_well)
        self._safe_connect("actionRemoveWell", "triggered", self._on_remove_well)

        # ---- Import/Export ----
        self._safe_connect("actionImportLAS", "triggered", self._browse_las)
        self._safe_connect("actionImportCSV", "triggered", self._browse_csv)
        self._safe_connect("actionImportDLIS", "triggered", self._browse_dlis)
        self._safe_connect("actionExportPDF", "triggered", self._on_export_pdf)
        self._safe_connect("actionExportCSV", "triggered", self._on_export_csv)

        # ---- View menu (switch central tabs) ----
        self._safe_connect("actionViewLogPlot", "triggered", self._on_zoom_in)
        self._safe_connect("actionViewCrossPlot", "triggered", self._on_zoom_out)
        self._safe_connect("actionViewHistogram", "triggered", self._on_zoom_reset)

        # ---- Calculation menu ----
        self._safe_connect("actionCalcAll", "triggered", self._on_calc_all)
        self._safe_connect("actionCalcVSH", "triggered", self._on_calc_vsh)
        self._safe_connect("actionCalcPorosity", "triggered", self._on_calc_porosity)
        self._safe_connect("actionCalcSaturation", "triggered", self._on_calc_sw)
        self._safe_connect("actionCalcNetPay", "triggered", self._on_calc_net_pay)

        # ---- Import tab buttons ----
        self._safe_connect("lasBrowseBtn", "clicked", self._browse_las)
        self._safe_connect("lasLoadBtn", "clicked", self._load_las)
        self._safe_connect("csvBrowseBtn", "clicked", self._browse_csv)
        self._safe_connect("csvLoadBtn", "clicked", self._load_csv)
        self._safe_connect("dlisBrowseBtn", "clicked", self._browse_dlis)
        self._safe_connect("dlisLoadBtn", "clicked", self._load_dlis)
        self._safe_connect("lisBrowseBtn", "clicked", self._browse_lis)
        self._safe_connect("lisLoadBtn", "clicked", self._load_lis)

        # ---- Well browser panel ----
        self._safe_connect("addWellBtn", "clicked", self._on_add_well)
        self._safe_connect("removeWellBtn", "clicked", self._on_remove_well)
        self._safe_connect("addTopBtn", "clicked", self._on_add_top)
        self._safe_connect("deleteTopBtn", "clicked", self._on_del_top)

        # ---- Centre panel plot buttons ----
        self._safe_connect("plotLogsBtn", "clicked", self._on_plot_logs)
        self._safe_connect("exportLogsBtn", "clicked", self._on_export_pdf)
        self._safe_connect("crossPlotBtn", "clicked", self._on_plot_cross)
        self._safe_connect("histPlotBtn", "clicked", self._on_plot_hist)
        self._safe_connect("statsCalcBtn", "clicked", self._on_calc_stats)
        self._safe_connect("statsExportBtn", "clicked", self._on_export_csv)
        self._safe_connect("mwCompareBtn", "clicked", self._on_plot_mw)

        # ---- Right panel calc buttons ----
        self._safe_connect("vshCalcBtn", "clicked", self._on_calc_vsh)
        self._safe_connect("porCalcBtn", "clicked", self._on_calc_porosity)
        self._safe_connect("satCalcBtn", "clicked", self._on_calc_sw)
        self._safe_connect("emCalcBtn", "clicked", self._on_calc_elastic)
        self._safe_connect("lithoClassifyBtn", "clicked", self._on_classify_litho)
        self._safe_connect("runQcBtn", "clicked", self._on_run_qc)
        self._safe_connect("npCalcBtn", "clicked", self._on_calc_net_pay)

    def _safe_connect(self, widget_name: str, signal_name: str, slot):
        """Connect a widget signal to a slot, ignoring missing widgets."""
        widget = self.findChild(object, widget_name)
        if widget is None:
            return
        signal = getattr(widget, signal_name, None)
        if signal is not None:
            signal.connect(slot)

    # ------------------------------------------------------------------
    # Default population helpers
    # ------------------------------------------------------------------
    def _populate_defaults(self):
        """Populate combo boxes and lists with default items."""
        # X/Y axis combo boxes for cross-plot
        log_curves = [
            "GR", "NPHI", "RHOB", "DT", "RT", "RXO", "PE",
            "CAL", "SP", "VSH", "PHIE", "SW", "PERM",
        ]
        for name in ("xAxisCombo", "yAxisCombo", "colorByCombo",
                     "histCurveCombo", "mwCurveCombo"):
            cb = self.findChild(object, name)
            if cb is not None:
                cb.addItems(log_curves)

        # Stats zone
        zone_cb = self.findChild(object, "statsZoneCombo")
        if zone_cb is not None:
            zone_cb.addItems(["All Zones", "Zone A", "Zone B", "Zone C"])

        # Multi-well align
        mw_align = self.findChild(object, "mwAlignCombo")
        if mw_align is not None:
            mw_align.addItems(["KB Depth", "TVDSS", "Formation Top"])

        # Active well combo
        well_cb = self.findChild(object, "activeWellCombo")
        if well_cb is not None:
            well_cb.addItem("-- No well loaded --")

        self._set_status("Ready")

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------
    def _set_status(self, msg: str):
        QtWidgets.QMainWindow.statusBar(self).showMessage(f"PetroAnalyst Pro  |  {msg}")

    def _set_progress(self, value: int):
        if hasattr(self, "_progress_bar"):
            self._progress_bar.setValue(value)

    # ------------------------------------------------------------------
    # File menu handlers
    # ------------------------------------------------------------------
    def _on_new_project(self):
        self._set_status("New project created")
        QMessageBox.information(self, "New Project", "New project created.")

    def _on_open_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Petrophysics Project (*.ppro *.json);;All Files (*)"
        )
        if path:
            self._set_status(f"Project loaded: {os.path.basename(path)}")

    def _on_save_project(self):
        self._set_status("Project saved")
        QMessageBox.information(self, "Save Project", "Project saved successfully.")

    # ------------------------------------------------------------------
    # Well management
    # ------------------------------------------------------------------
    def _on_add_well(self):
        name, ok = QtWidgets.QInputDialog.getText(
            self, "Add Well", "Enter well name:"
        )
        if ok and name.strip():
            self._set_status(f"Well added: {name.strip()}")
            # Add to active well combo
            well_cb = self.findChild(object, "activeWellCombo")
            if well_cb is not None:
                if well_cb.count() == 1 and well_cb.itemText(0) == "-- No well loaded --":
                    well_cb.clear()
                well_cb.addItem(name.strip())

    def _on_remove_well(self):
        well_cb = self.findChild(object, "activeWellCombo")
        if well_cb is not None and well_cb.count() > 0:
            name = well_cb.currentText()
            well_cb.removeItem(well_cb.currentIndex())
            self._set_status(f"Well removed: {name}")

    def _on_add_top(self):
        tbl = self.findChild(object, "formationTopsTable")
        if tbl is not None:
            row = tbl.rowCount()
            tbl.insertRow(row)
            tbl.setItem(row, 0, QtWidgets.QTableWidgetItem("New Formation"))
            tbl.setItem(row, 1, QtWidgets.QTableWidgetItem("0.0"))

    def _on_del_top(self):
        tbl = self.findChild(object, "formationTopsTable")
        if tbl is not None and tbl.currentRow() >= 0:
            tbl.removeRow(tbl.currentRow())

    # ------------------------------------------------------------------
    # Import handlers
    # ------------------------------------------------------------------
    def _browse_file(self, line_edit_name: str, caption: str, file_filter: str):
        path, _ = QFileDialog.getOpenFileName(self, caption, "", file_filter)
        if path:
            le = self.findChild(object, line_edit_name)
            if le is not None:
                le.setText(path)
        return path

    def _browse_las(self):
        self._browse_file(
            "lasPathEdit",
            "Select LAS File",
            "LAS Files (*.las *.LAS);;All Files (*)"
        )

    def _browse_csv(self):
        self._browse_file(
            "csvPathEdit",
            "Select CSV/Excel File",
            "CSV/Excel Files (*.csv *.xlsx *.xls);;All Files (*)"
        )

    def _browse_dlis(self):
        self._browse_file(
            "dlisPathEdit",
            "Select DLIS File",
            "DLIS Files (*.dlis *.DLIS);;All Files (*)"
        )

    def _browse_lis(self):
        self._browse_file(
            "lisPathEdit",
            "Select Well Log File",
            "Log Files (*.lis *.txt *.sap *.asc);;All Files (*)"
        )

    def _get_path(self, line_edit_name: str) -> str:
        le = self.findChild(object, line_edit_name)
        return le.text().strip() if le else ""

    def _append_import_log(self, msg: str):
        te = self.findChild(object, "importLogText")
        if te is not None:
            te.append(msg)

    def _load_las(self):
        path = self._get_path("lasPathEdit")
        if not path:
            QMessageBox.warning(self, "No File", "Please select a LAS file first.")
            return
        self._set_progress(10)
        self._set_status(f"Loading LAS: {os.path.basename(path)}")
        try:
            import lasio
            las = lasio.read(path)
            self._set_progress(100)
            self._append_import_log(
                f"[OK] Loaded {os.path.basename(path)} — "
                f"{len(las.curves)} curves, depth {las.index[0]:.1f}–{las.index[-1]:.1f} m"
            )
            self._set_status(f"LAS loaded: {os.path.basename(path)}")
        except Exception as exc:
            self._set_progress(0)
            self._append_import_log(f"[ERROR] {exc}")
            QMessageBox.critical(self, "Import Error", str(exc))

    def _load_csv(self):
        path = self._get_path("csvPathEdit")
        if not path:
            QMessageBox.warning(self, "No File", "Please select a CSV/Excel file first.")
            return
        self._set_progress(10)
        self._set_status(f"Loading CSV: {os.path.basename(path)}")
        try:
            import pandas as pd
            df = pd.read_csv(path) if path.lower().endswith(".csv") else pd.read_excel(path)
            self._set_progress(100)
            self._append_import_log(
                f"[OK] Loaded {os.path.basename(path)} — "
                f"{len(df.columns)} columns, {len(df)} rows"
            )
            self._set_status(f"CSV loaded: {os.path.basename(path)}")
        except Exception as exc:
            self._set_progress(0)
            self._append_import_log(f"[ERROR] {exc}")
            QMessageBox.critical(self, "Import Error", str(exc))

    def _load_dlis(self):
        path = self._get_path("dlisPathEdit")
        if not path:
            QMessageBox.warning(self, "No File", "Please select a DLIS file first.")
            return
        self._set_progress(10)
        self._set_status(f"Loading DLIS: {os.path.basename(path)}")
        try:
            from dlisio import dlis as dlisio
            f, *tail = dlisio.load(path)
            self._set_progress(100)
            self._append_import_log(
                f"[OK] Loaded {os.path.basename(path)} — "
                f"{len(list(f.channels))} channels"
            )
            self._set_status(f"DLIS loaded: {os.path.basename(path)}")
        except Exception as exc:
            self._set_progress(0)
            self._append_import_log(f"[ERROR] {exc}")
            QMessageBox.critical(self, "Import Error", str(exc))

    def _load_lis(self):
        path = self._get_path("lisPathEdit")
        if not path:
            QMessageBox.warning(self, "No File", "Please select a file first.")
            return
        self._set_progress(50)
        self._set_status(f"Loading: {os.path.basename(path)}")
        self._append_import_log(f"[OK] Queued for import: {os.path.basename(path)}")
        self._set_progress(100)

    # ------------------------------------------------------------------
    # Export handlers
    # ------------------------------------------------------------------
    def _on_export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export to PDF", "", "PDF Files (*.pdf)"
        )
        if path:
            self._set_status(f"Exported PDF: {os.path.basename(path)}")
            QMessageBox.information(self, "Export", f"Saved to:\n{path}")

    def _on_export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "", "CSV Files (*.csv)"
        )
        if path:
            self._set_status(f"Exported CSV: {os.path.basename(path)}")
            QMessageBox.information(self, "Export", f"Saved to:\n{path}")

    # ------------------------------------------------------------------
    # View handlers
    # ------------------------------------------------------------------
    def _on_zoom_in(self):
        self._set_status("Zoom in")

    def _on_zoom_out(self):
        self._set_status("Zoom out")

    def _on_zoom_reset(self):
        self._set_status("Zoom reset")

    # ------------------------------------------------------------------
    # Plot handlers
    # ------------------------------------------------------------------
    def _on_plot_logs(self):
        self._set_status("Plotting well logs...")

    def _on_plot_cross(self):
        self._set_status("Generating cross plot...")

    def _on_plot_hist(self):
        self._set_status("Generating histogram...")

    def _on_calc_stats(self):
        self._set_status("Calculating depth statistics...")

    def _on_plot_mw(self):
        self._set_status("Generating multi-well comparison...")

    # ------------------------------------------------------------------
    # Calculation handlers
    # ------------------------------------------------------------------
    def _on_calc_all(self):
        self._set_status("Running all petrophysical calculations...")

    def _on_calc_vsh(self):
        self._set_status("Calculating Shale Volume (Vsh)...")

    def _on_calc_porosity(self):
        self._set_status("Calculating Effective Porosity (PHIE)...")

    def _on_calc_sw(self):
        self._set_status("Calculating Water Saturation (Sw)...")

    def _on_calc_elastic(self):
        self._set_status("Calculating elastic parameters...")

    def _on_classify_litho(self):
        self._set_status("Classifying lithology...")

    def _on_run_qc(self):
        self._set_status("Running quality control checks...")

    def _on_calc_net_pay(self):
        self._set_status("Calculating Net Pay / NTG...")


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PetroAnalyst Pro")
    app.setOrganizationName("PetroAnalyst")

    # High-DPI support
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    window = PetroAnalystMain()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
