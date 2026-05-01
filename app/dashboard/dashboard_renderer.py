from PyQt5.QtWidgets import (
    QTableWidgetItem, QPushButton, QWidget, QHBoxLayout,
    QDialog, QTableWidget, QAbstractItemView,
)
from util.dashboard_util import DashboardFormatter
from util.edit_record_dialog_util import EditRecordDialog

from PyQt5.QtCore import Qt, QPoint, QObject, QEvent
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

        self._records        = []
        self._is_dragging    = False
        self._drag_start_row = -1
        self.selected_row    = -1
        self.selected_record = None
        self._selected_rows  = set()

        self.table.viewport().installEventFilter(self)
        
    def eventFilter(self, obj, event) -> bool:
        if obj is self.table.viewport():
            if event.type() == QEvent.MouseButtonPress:
                self._on_press(event)
            elif event.type() == QEvent.MouseMove:
                self._on_move(event)
            elif event.type() == QEvent.MouseButtonRelease:
                self._on_release(event)
        return False  # never consume — Edit button clicks still work
    # ── Public ────────────────────────────────────────────────────────────────

    def clear(self):
        self.table.setRowCount(0)
        self._records.clear()
        self._selected_rows.clear()
        self._reset_drag()
        self.selected_row    = -1
        self.selected_record = None

    def render(self, records: list):
        self.clear()
        self._records = list(records)

        for row_idx, r in enumerate(self._records):
            self.table.insertRow(row_idx)

            btn_edit = QPushButton("Edit")
            btn_edit.setFixedWidth(80)
            btn_edit.setStyleSheet(btn_style)
            btn_edit.clicked.connect(lambda _, rec=r: self._open_edit_dialog(rec))

            date       = DashboardFormatter.format_date(
                r.get('date',''), r.get('month',''), r.get('year','')
            )
            time_range = DashboardFormatter.format_time_range(
                r.get('start_time','n/a'), r.get('end_time','n/a'), r.get('meridiem','n/a')
            )

            self._set_cell(row_idx, 0, r.get('admin_under') or 'n/a')
            self._set_cell(row_idx, 1, date)
            self._set_cell(row_idx, 2, r.get('client_name'))
            self._set_cell(row_idx, 3, time_range)
            self._set_cell(row_idx, 4, DashboardFormatter.format_chemicals(r.get('chemicals_use')))
            self._set_cell(row_idx, 5, DashboardFormatter.format_chemicals(r.get('actual_chemicals_used'), True))
            self._set_cell(row_idx, 6, r.get('remarks') or 'n/a')
            self._set_cell(row_idx, 7, btn_edit)

    # ── Mouse events (viewport-relative coordinates) ──────────────────────────

    def _on_press(self, event):
        print(f"[PRESS] button={event.button()}, pos={event.pos()}")
        if event.button() == Qt.LeftButton:
            row = self._row_at(event.pos())
            print(f"[PRESS] row_at={row}, total_rows={self.table.rowCount()}")
            if row >= 0:
                self._is_dragging    = True
                self._drag_start_row = row
                self._clear_all_highlights()
                self._selected_rows  = {row}
                self._highlight_row(row, _SELECTED_COLOR)
                self.selected_row    = row
                self.selected_record = self._safe_record(row)
                print(f"[PRESS] selected record={self.selected_record}")

    def _on_move(self, event):
        if not (self._is_dragging and event.buttons() & Qt.LeftButton):
            return

        current_row = self._row_at(event.pos())
        if current_row < 0:
            return

        top    = min(self._drag_start_row, current_row)
        bottom = max(self._drag_start_row, current_row)
        new_selected = set(range(top, bottom + 1))

        # Only repaint changed rows — no flicker
        for row in self._selected_rows - new_selected:
            self._highlight_row(row, _DEFAULT_COLOR)
        for row in new_selected - self._selected_rows:
            self._highlight_row(row, _SELECTED_COLOR)

        self._selected_rows  = new_selected
        self.selected_row    = current_row
        self.selected_record = self._safe_record(current_row)

    def _on_release(self, event):
        if event.button() == Qt.LeftButton and self._is_dragging:
            end_row = self._row_at(event.pos())

            # ── Single-click on the Edit column → open dialog, skip selection ──
            if end_row == self._drag_start_row:
                col = self.table.columnAt(event.pos().x())
                if col == 7:                          # Edit column index
                    rec = self._safe_record(end_row)
                    if rec:
                        self._reset_drag()
                        self._open_edit_dialog(rec)
                        return

            # ── Multi-row drag or click on non-Edit column → select rows ──
            if end_row >= 0:
                top    = min(self._drag_start_row, end_row)
                bottom = max(self._drag_start_row, end_row)

                self._clear_all_highlights()
                self._selected_rows = set(range(top, bottom + 1))
                for row in self._selected_rows:
                    self._highlight_row(row, _SELECTED_COLOR)

                self.selected_row    = end_row
                self.selected_record = self._safe_record(end_row)

            self._reset_drag()

    # ── Row detection ─────────────────────────────────────────────────────────

    def _row_at(self, viewport_pos: QPoint) -> int:
        row = self.table.rowAt(viewport_pos.y())
        print(f"[ROW_AT] y={viewport_pos.y()}, rowAt={row}")
        if row >= 0:
            return row

        scroll_offset = self.table.verticalScrollBar().value()
        content_y     = viewport_pos.y() + scroll_offset
        header_height = self.table.horizontalHeader().height()
        y = content_y - header_height
        print(f"[ROW_AT] fallback: scroll={scroll_offset}, content_y={content_y}, header_h={header_height}, y={y}")

        if y < 0:
            return -1

        cumulative = 0
        for r in range(self.table.rowCount()):
            cumulative += self.table.rowHeight(r)
            if y < cumulative:
                return r

        return -1

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _safe_record(self, row: int):
        return self._records[row] if 0 <= row < len(self._records) else None

    def _highlight_row(self, row: int, color: QColor):
        is_selected = color != _DEFAULT_COLOR

        for col in range(self.table.columnCount()):
            # ── QTableWidgetItem cells ────────────────────────────────────────
            item = self.table.item(row, col)
            if item:
                item.setBackground(color)

            # ── Cell widget containers ────────────────────────────────────────
            widget = self.table.cellWidget(row, col)
            if widget:
                if is_selected:
                    # Color the container AND every child button inside it
                    widget.setStyleSheet(
                        f"QWidget {{ background-color: {color.name()}; }}"
                        f"QPushButton {{ background-color: #cc3333; color: white; "
                        f"border-radius: 6px; padding: 6px; }}"
                    )
                else:
                    widget.setStyleSheet("")  # restore to btn_style

        # ── Vertical header ───────────────────────────────────────────────────
        v_header = self.table.verticalHeaderItem(row)
        if v_header:
            v_header.setBackground(color if is_selected else QColor("#F0F0F0"))
            v_header.setForeground(QColor("#1B4332"))

    def _clear_all_highlights(self):
        for row in range(self.table.rowCount()):
            self._highlight_row(row, _DEFAULT_COLOR)
        self._selected_rows.clear()

    def _clear_selection(self):
        self._clear_all_highlights()
        self.selected_row    = -1
        self.selected_record = None

    def _reset_drag(self):
        self._is_dragging    = False
        self._drag_start_row = -1

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

            # ✅ Let mouse press/move/release fall through to the viewport
            #    so the row-drag event filter still fires correctly.
            container.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            value.setAttribute(Qt.WA_TransparentForMouseEvents, True)

            self.table.setCellWidget(row, col, container)
        else:
            self.table.setItem(row, col, QTableWidgetItem(str(value)))