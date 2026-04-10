from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout
from util.dashboard_util import DashboardFormatter
from PyQt5.QtCore import Qt
from ui.trash_btn import btn_style

class DashboardTableRenderer:
    def __init__(self, table, on_trash_callback):
        self.table = table
        self.on_trash = on_trash_callback

    def clear(self):
        self.table.setRowCount(0)

    def _set_cell(self, row, col, value):
        if isinstance(value, QPushButton):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.addWidget(value)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, col, container)
        else:
            self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def render(self, records):
        self.clear()

        for row_idx, r in enumerate(records):
            self.table.insertRow(row_idx)

            btn = QPushButton("Trash")
            btn.setFixedSize(80, 28)
            btn.setStyleSheet(btn_style)
            btn.clicked.connect(lambda _, rid=r.get('id'): self.on_trash(rid))

            date = DashboardFormatter.format_date(
                r.get('date', ''),
                r.get('month', ''),
                r.get('year', '')
            )

            time_range = DashboardFormatter.format_time_range(
                r.get('start_time', 'n/a'),
                r.get('end_time', 'n/a'),
                r.get('meridiem', 'n/a')
            )

            self._set_cell(0, 0, r.get('admin_under') or 'n/a')
            self._set_cell(0, 1, date)
            self._set_cell(0, 2, r.get('client_name'))
            self._set_cell(0, 3, time_range)
            self._set_cell(0, 4, DashboardFormatter.format_chemicals(r.get('chemicals_use')))
            self._set_cell(0, 5, DashboardFormatter.format_chemicals(r.get('actual_chemicals_used'), True))
            self._set_cell(0, 6, btn)