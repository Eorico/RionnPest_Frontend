from PyQt5.QtWidgets import (
    QTableWidgetItem, QPushButton, QWidget, QHBoxLayout,
    QDialog,
)
from util.dashboard_util import DashboardFormatter
from util.edit_record_dialog_util import EditRecordDialog
from util.check_box_util import _GreenCheckBox
from util.table_util import TableDataHelper

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QColor
from ui.style import btn_style, _BTN_EDIT_LOCKED

_SELECTED_COLOR = QColor("#A8D5BA")
_DEFAULT_COLOR  = QColor(Qt.white)
_BTN_EDIT_OWNED = btn_style


class DashboardTableRenderer(QObject):
    def __init__(self, table, on_trash_callback, on_edit_callback, current_admin=None):
        super().__init__()
        self.table         = table
        self.on_trash      = on_trash_callback
        self.on_edit       = on_edit_callback
        self._records      = []
        self.current_admin = (current_admin or "").strip().lower() 

    # ── Public ────────────────────────────────────────────────────────────────

    def update_admin(self, admin: str):
        """Refresh the stored admin after login completes."""
        self.current_admin = (admin or "").strip().lower()

    def _sync_checkbox_column(self):
        has_data = self.table.rowCount() > 0
        self.table.setColumnHidden(0, not has_data)

    def clear(self):
        self.table.setRowCount(0)
        self._records.clear()
        self._sync_checkbox_column()

    def render(self, records: list):
        self.clear()
        self._records = list(records)

        for row_idx, r in enumerate(self._records):
            self.table.insertRow(row_idx)

            row_admin = (r.get('admin_under') or "").strip().lower()
            is_owner  = bool(self.current_admin) and (row_admin == self.current_admin)
 
            self._set_checkbox(row_idx, is_owner)

            btn_edit = QPushButton("Edit")
            btn_edit.setFixedWidth(80)

            if is_owner:
                btn_edit.setStyleSheet(_BTN_EDIT_OWNED)
                btn_edit.setCursor(Qt.PointingHandCursor)
                btn_edit.setToolTip("Edit this record")
                btn_edit.clicked.connect(lambda _, rec=r: self._open_edit_dialog(rec))
            else:
                btn_edit.setStyleSheet(_BTN_EDIT_LOCKED)
                btn_edit.setCursor(Qt.ForbiddenCursor)
                btn_edit.setEnabled(False)
                btn_edit.setToolTip(f"Owned by {row_admin or 'another admin'} — you cannot edit this")

            self._set_cell(row_idx, 1, r.get('admin_under') or 'n/a')
            self._set_cell(row_idx, 2, TableDataHelper.fmt_date(r))
            self._set_cell(row_idx, 3, r.get('client_name') or 'n/a')
            self._set_cell(row_idx, 4, TableDataHelper.fmt_time_range(r))
            self._set_cell(row_idx, 5, TableDataHelper.fmt_chemicals(TableDataHelper.get_chemicals(r)))
            self._set_cell(row_idx, 6, TableDataHelper.fmt_chemicals(TableDataHelper.get_actual_chemicals(r), True))
            self._set_cell(row_idx, 7, TableDataHelper.fmt_remarks(r))
            self._set_action_cell(row_idx, 8, btn_edit)

            if not is_owner:
                self._dim_row(row_idx)

        self._sync_checkbox_column()

    # ── Checkbox helpers ──────────────────────────────────────────────────────

    def _set_checkbox(self, row: int, is_owner: bool = True):   
        cb = _GreenCheckBox()
        cb.setFixedSize(26, 26)

        if is_owner:
            cb.setCursor(Qt.PointingHandCursor)
            cb.setToolTip("Select this record")
            cb.stateChanged.connect(lambda state, r=row: self._on_checkbox_changed(r, state))
        else:
            cb.setEnabled(False)
            cb.setCursor(Qt.ForbiddenCursor)
            cb.setToolTip("You cannot select another admin's record")   
            cb.setStyleSheet("""
                QCheckBox::indicator {
                    width: 18px; height: 18px;
                    border: 2px solid #D1D5DB;
                    border-radius: 4px;
                    background: #F3F4F6;
                }
            """)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(cb)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        container.setStyleSheet("background-color: #FFFFFF;")

        def container_mouse_press(event, _is_owner=is_owner):
            if not _is_owner:
                return
            if event.button() == Qt.LeftButton:
                cb.setChecked(not cb.isChecked())

        container.mousePressEvent = container_mouse_press
        self.table.setCellWidget(row, 0, container)

    def _on_checkbox_changed(self, row: int, state: int):
        color = _SELECTED_COLOR if state == Qt.Checked else _DEFAULT_COLOR
        self._highlight_row(row, color)

    def _get_checkbox(self, row: int):
        container = self.table.cellWidget(row, 0)
        if container:
            for child in container.children():
                if isinstance(child, _GreenCheckBox):
                    return child
        return None

    # ── Selection queries ─────────────────────────────────────────────────────

    @property
    def selected_record(self):
        records = self.get_checked_records()
        return records[0] if records else None

    def get_checked_records(self) -> list:
        result = []
        for row in range(self.table.rowCount()):
            cb = self._get_checkbox(row)
            if cb and cb.isChecked():
                rec = self._safe_record(row)
                if rec:
                    result.append(rec)
        return result

    def get_checked_rows(self) -> list:
        return [
            row for row in range(self.table.rowCount())
            if (cb := self._get_checkbox(row)) and cb.isChecked()
        ]

    def clear_all_checks(self):
        for row in range(self.table.rowCount()):
            cb = self._get_checkbox(row)
            if cb:
                cb.blockSignals(True)
                cb.setChecked(False)
                cb.blockSignals(False)
            self._highlight_row(row, _DEFAULT_COLOR)

    # ── Highlight ─────────────────────────────────────────────────────────────

    def _highlight_row(self, row: int, color: QColor):
        is_selected = color != _DEFAULT_COLOR

        for col in range(self.table.columnCount()):
            if col == 0 or col == 8:
                widget = self.table.cellWidget(row, col)
                if widget:
                    widget.setStyleSheet("background-color: #FFFFFF;")
                continue

            item = self.table.item(row, col)
            if item:
                item.setBackground(color)

            widget = self.table.cellWidget(row, col)
            if widget:
                if is_selected:
                    widget.setStyleSheet(
                        f"QWidget {{ background-color: {color.name()}; }}"
                        f"QPushButton {{ background-color: #cc3333; color: white; "
                        f"border-radius: 6px; padding: 6px; }}"
                    )
                else:
                    widget.setStyleSheet("background-color: #FFFFFF;")

        v_header = self.table.verticalHeaderItem(row)
        if v_header:
            v_header.setBackground(color if is_selected else QColor("#F0F0F0"))
            v_header.setForeground(QColor("#1B4332"))

    def _dim_row(self, row: int):  
        muted      = QColor("#F3F4F6")
        muted_text = QColor("#9CA3AF")
        for col in range(1, 8):  
            item = self.table.item(row, col)
            if item:
                item.setBackground(muted)
                item.setForeground(muted_text)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _safe_record(self, row: int):
        return self._records[row] if 0 <= row < len(self._records) else None

    def _open_edit_dialog(self, record: dict):
        dlg = EditRecordDialog(record, parent=self.table)
        if dlg.exec_() == QDialog.Accepted:
            self.on_edit(dlg.get_data())

    def _set_action_cell(self, row, col, btn_edit):
        container = QWidget()
        layout    = QHBoxLayout(container)
        layout.addWidget(btn_edit)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(4)
        container.setStyleSheet("background-color: #FFFFFF;")
        self.table.setCellWidget(row, col, container)

    def _set_cell(self, row, col, value):
        if isinstance(value, QPushButton):
            container = QWidget()
            layout    = QHBoxLayout(container)
            layout.addWidget(value)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            container.setStyleSheet("background-color: #FFFFFF;")
            self.table.setCellWidget(row, col, container)
        else:
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.table.setItem(row, col, item)