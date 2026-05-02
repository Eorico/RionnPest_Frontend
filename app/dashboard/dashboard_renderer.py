from PyQt5.QtWidgets import (
    QTableWidgetItem, QPushButton, QWidget, QHBoxLayout,
    QDialog,
)
from util.dashboard_util import DashboardFormatter
from util.edit_record_dialog_util import EditRecordDialog
from util.check_box_util import _GreenCheckBox

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QColor
from ui.style import btn_style

_SELECTED_COLOR = QColor("#A8D5BA")
_DEFAULT_COLOR  = QColor(Qt.white)


class DashboardTableRenderer(QObject):
    def __init__(self, table, on_trash_callback, on_edit_callback):
        super().__init__()
        self.table    = table
        self.on_trash = on_trash_callback
        self.on_edit  = on_edit_callback
        self._records = []

    # ── Public ────────────────────────────────────────────────────────────────
    
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

            self._set_checkbox(row_idx)

            btn_edit = QPushButton("Edit")
            btn_edit.setFixedWidth(80)
            btn_edit.setStyleSheet(btn_style)
            btn_edit.clicked.connect(lambda _, rec=r: self._open_edit_dialog(rec))
            
            chem_remarks   = [f"[C.U]: {c.get('remarks')}"     for c in (r.get('chemicals_use') or [])        if (c.get('remarks') or '').strip()]
            actual_remarks = [f"[A.C.U]: {c.get('remarks')}"   for c in (r.get('actual_chemicals_used') or []) if (c.get('remarks') or '').strip()]
            all_remarks    = chem_remarks + actual_remarks
            
            date = DashboardFormatter.format_date(
                r.get('date', ''), 
                r.get('month', ''), 
                r.get('year', '')
            )
            time_range = DashboardFormatter.format_time_range(
                r.get('start_time', 'n/a'),
                r.get('end_time', 'n/a'),
                r.get('start_meridiem', 'n/a'),
                r.get('end_meridiem', 'n/a')
            )

            self._set_cell(row_idx, 1, r.get('admin_under') or 'n/a')
            self._set_cell(row_idx, 2, date)
            self._set_cell(row_idx, 3, r.get('client_name'))
            self._set_cell(row_idx, 4, time_range)
            self._set_cell(row_idx, 5, DashboardFormatter.format_chemicals(r.get('chemicals_use')))
            self._set_cell(row_idx, 6, DashboardFormatter.format_chemicals(r.get('actual_chemicals_used'), True))
            self._set_cell(row_idx, 7, "\n".join(all_remarks) if all_remarks else "n/a")
            self._set_cell(row_idx, 8, btn_edit)
            
        self._sync_checkbox_column()

    # ── Checkbox helpers ──────────────────────────────────────────────────────

    def _set_checkbox(self, row: int):
        cb = _GreenCheckBox()
        cb.setFixedSize(26, 26)
        cb.setCursor(Qt.PointingHandCursor)
        cb.stateChanged.connect(lambda state, r=row: self._on_checkbox_changed(r, state))

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(cb)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        # ✅ Force white — stops scrollArea's QWidget cascade from tinting it
        container.setStyleSheet("background-color: #FFFFFF;")

        def container_mouse_press(event):
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
            # ── Col 0 (checkbox) and col 8 (edit) always stay white ──────────────
            if col == 0 or col == 8:
                widget = self.table.cellWidget(row, col)
                if widget:
                    widget.setStyleSheet("background-color: #FFFFFF;")
                continue  # skip item background too — no tint on these columns

            # ── Data columns 1–7: apply or remove highlight ───────────────────────
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

        # ── Vertical header ───────────────────────────────────────────────────────
        v_header = self.table.verticalHeaderItem(row)
        if v_header:
            v_header.setBackground(color if is_selected else QColor("#F0F0F0"))
            v_header.setForeground(QColor("#1B4332"))

    # ── Internals ─────────────────────────────────────────────────────────────

    def _safe_record(self, row: int):
        return self._records[row] if 0 <= row < len(self._records) else None

    def _open_edit_dialog(self, record: dict):
        dlg = EditRecordDialog(record, parent=self.table)
        if dlg.exec_() == QDialog.Accepted:
            self.on_edit(dlg.get_data())

    def _set_cell(self, row, col, value):
        if isinstance(value, QPushButton):
            container = QWidget()
            layout    = QHBoxLayout(container)
            layout.addWidget(value)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            # ✅ Force white background on all button containers from the start
            container.setStyleSheet("background-color: #FFFFFF;")
            self.table.setCellWidget(row, col, container)
        else:
            self.table.setItem(row, col, QTableWidgetItem(str(value)))