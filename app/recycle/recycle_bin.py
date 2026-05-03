from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox,
    QWidget, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from ui.recycle_bin import Ui_RecycleBin
from util.table_util import TableDataHelper
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(os.path.dirname(CURRENT_DIR), "ui", "assets")


class RecyclBinWindow(QMainWindow):
    def __init__(self, api_service, on_restore_callback=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_RecycleBin()
        self.ui.setupUi(self)
        self.api = api_service
        self.on_restore_callback = on_restore_callback
        self._records = []

        self.setWindowIcon(QIcon(f"{IMAGE_PATH}/Logo.png"))

        self.ui.Restore_btn.clicked.connect(self.handle_restore)
        self.ui.Restore_all_btn.clicked.connect(self.handle_restore_all)
        self.ui.Delete_permanently_btn.clicked.connect(self.handle_permanent_delete_restore)

        self.ui.recycle_table.setColumnCount(9)  # +1 for remarks
        self.ui.recycle_table.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        self.ui.recycle_table.setHorizontalHeaderItem(1, QTableWidgetItem("Category"))
        self.ui.recycle_table.setHorizontalHeaderItem(2, QTableWidgetItem("Admin"))
        self.ui.recycle_table.setHorizontalHeaderItem(3, QTableWidgetItem("Date"))
        self.ui.recycle_table.setHorizontalHeaderItem(4, QTableWidgetItem("Client"))
        self.ui.recycle_table.setHorizontalHeaderItem(5, QTableWidgetItem("Time"))
        self.ui.recycle_table.setHorizontalHeaderItem(6, QTableWidgetItem("Chemicals Used"))
        self.ui.recycle_table.setHorizontalHeaderItem(7, QTableWidgetItem("Actual Chemicals"))
        self.ui.recycle_table.setHorizontalHeaderItem(8, QTableWidgetItem("Remarks"))

        self.ui.recycle_table.setColumnWidth(0, 50)
        self.ui.recycle_table.setColumnWidth(5, 300)
        self.ui.recycle_table.setColumnWidth(6, 400)
        self.ui.recycle_table.setColumnWidth(7, 400)
        self.ui.recycle_table.setColumnWidth(8, 250)
        self.ui.recycle_table.setColumnHidden(0, True)  # hidden until data loads

        self.ui.recycle_table.setWordWrap(True)
        self.ui.recycle_table.verticalHeader().setSectionResizeMode(
            self.ui.recycle_table.verticalHeader().ResizeToContents
        )

        self.load_bin_data_restore()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_bin_data_restore()

    def load_bin_data_restore(self):
        self._records = self.api.get_recycle_bin()
        self.ui.recycle_table.setRowCount(0)

        for row, r in enumerate(self._records):
            self.ui.recycle_table.insertRow(row)
            self._set_checkbox(row, r)

            cat_item = QTableWidgetItem(r.get('category', 'Unknown'))
            cat_item.setData(Qt.UserRole, r.get('id'))

            self.ui.recycle_table.setItem(row, 1, cat_item)
            self.ui.recycle_table.setItem(row, 2, QTableWidgetItem(r.get('admin_under') or 'n/a'))
            self.ui.recycle_table.setItem(row, 3, QTableWidgetItem(TableDataHelper.fmt_date(r)))
            self.ui.recycle_table.setItem(row, 4, QTableWidgetItem(r.get('client_name', '')))
            self.ui.recycle_table.setItem(row, 5, QTableWidgetItem(TableDataHelper.fmt_time_range(r)))
            self.ui.recycle_table.setItem(row, 6, QTableWidgetItem(
                TableDataHelper.fmt_chemicals(TableDataHelper.get_chemicals(r))))
            self.ui.recycle_table.setItem(row, 7, QTableWidgetItem(
                TableDataHelper.fmt_chemicals(TableDataHelper.get_actual_chemicals(r), True)))
            self.ui.recycle_table.setItem(row, 8, QTableWidgetItem(TableDataHelper.fmt_remarks(r)))

        self.ui.recycle_table.setColumnHidden(0, self.ui.recycle_table.rowCount() == 0)

    def _fmt_chemicals(self, data_list, is_actual=False):
        if not isinstance(data_list, list):
            return "n/a"
        parts = []
        for item in data_list:
            name = item.get('actual_chemicals_name') if is_actual else None
            name = name or item.get('chemical_name') or "Unknown"
            qty  = item.get('quantity', '0')
            prefix = "[A.C.U]" if is_actual else "[C]"
            parts.append(f"{prefix}: {name} - [Q]: {qty}")
        return "\n".join(parts) if parts else "n/a"

    # ── Checkbox ──────────────────────────────────────────────────────────────

    def _set_checkbox(self, row: int, record: dict):
        cb = QCheckBox()
        cb.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(cb)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        container.setStyleSheet("background-color: #FFFFFF;")
        cb.stateChanged.connect(lambda state, r=row: self._on_checkbox_changed(r, state))

        self.ui.recycle_table.setCellWidget(row, 0, container)

    def _on_checkbox_changed(self, row: int, state: int):
        color = QColor("#A8D5BA") if state == Qt.Checked else QColor(Qt.white)
        for col in range(1, self.ui.recycle_table.columnCount()):
            item = self.ui.recycle_table.item(row, col)
            if item:
                item.setBackground(color)

    def _get_checkbox(self, row: int):
        container = self.ui.recycle_table.cellWidget(row, 0)
        if container:
            for child in container.children():
                if isinstance(child, QCheckBox):
                    return child
        return None

    def _get_checked_ids(self) -> list:
        ids = []
        for row in range(self.ui.recycle_table.rowCount()):
            cb = self._get_checkbox(row)
            if cb and cb.isChecked():
                item = self.ui.recycle_table.item(row, 1)
                if item:
                    ids.append(item.data(Qt.UserRole))
        return ids

    def _clear_checks(self):
        for row in range(self.ui.recycle_table.rowCount()):
            cb = self._get_checkbox(row)
            if cb:
                cb.blockSignals(True)
                cb.setChecked(False)
                cb.blockSignals(False)
            for col in range(1, self.ui.recycle_table.columnCount()):
                item = self.ui.recycle_table.item(row, col)
                if item:
                    item.setBackground(QColor(Qt.white))

    # ── Handlers ──────────────────────────────────────────────────────────────

    def get_selected_id_restore(self):
        """Fallback: single row click selection."""
        selected_row = self.ui.recycle_table.currentRow()
        if selected_row > -1:
            item = self.ui.recycle_table.item(selected_row, 1)
            if item:
                return item.data(Qt.UserRole)
        return None

    def handle_restore(self):
        ids = self._get_checked_ids()
        if not ids:
            QMessageBox.warning(self, "No Selection", "Check at least one record to restore.")
            return
        for rec_id in ids:
            success, msg = self.api.restore_record(rec_id)
            if not success:
                QMessageBox.critical(self, "Error", f"Failed to restore {rec_id}: {msg}")
                return
        QMessageBox.information(self, "Success", f"{len(ids)} record(s) restored.")
        self.load_bin_data_restore()
        self._clear_checks()
        if self.on_restore_callback:
            self.on_restore_callback()

    def handle_restore_all(self):
        success, msg = self.api.restore_all()
        if success:
            QMessageBox.information(self, "Success", "All records restored.")
            self.load_bin_data_restore()
            if self.on_restore_callback:
                self.on_restore_callback()
        else:
            if "429" in str(msg):
                QMessageBox.critical(self, "Rate Limit Exceeded",
                    "Too fast — wait a minute before retrying.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to restore all: {msg}")

    def handle_permanent_delete_restore(self):
        ids = self._get_checked_ids()
        if not ids:
            QMessageBox.warning(self, "No Selection", "Check at least one record to delete.")
            return
        confirm = QMessageBox.question(
            self, "Confirm",
            f"Permanently delete {len(ids)} record(s)? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            for rec_id in ids:
                success, msg = self.api.permanent_delete(rec_id)
                if not success:
                    QMessageBox.critical(self, "Error", f"Failed to delete {rec_id}: {msg}")
                    return
            QMessageBox.information(self, "Done", f"{len(ids)} record(s) permanently deleted.")
            self.load_bin_data_restore()
            self._clear_checks()
            if self.on_restore_callback:
                self.on_restore_callback()