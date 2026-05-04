from PyQt5.QtWidgets import (
    QTableWidgetItem, QWidget, QDialog,
    QHBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QLabel, QTableWidget,
    QVBoxLayout, QHeaderView, QAbstractItemView, QStyledItemDelegate,
    QPushButton, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor

# ── Theme ─────────────────────────────────────────────────────────────────────
_CLR_BG          = "#F0FAF4"
_CLR_PRIMARY     = "#2F6B3F"
_CLR_PRIMARY_DK  = "#1B4332"
_CLR_ACCENT      = "#C6F6D5"
_CLR_TEXT        = "#1B4332"
_CLR_BORDER_TOP  = "#C6F6D5"
_CLR_BORDER_BOT  = "#2D6A4F"

_DIALOG_SS = f"""
QDialog {{
    background-color: {_CLR_BG};
}}
QLabel {{
    font: 10pt 'Segoe UI';
    color: {_CLR_TEXT};
    background: transparent;
}}
QLineEdit, QComboBox {{
    background: #FFFFFF;
    border-radius: 6px;
    padding: 5px 10px;
    font: 10pt 'Segoe UI';
    color: {_CLR_TEXT};
    border: 1.5px solid #A8D5BA;
    min-height: 30px;
    selection-background-color: #C6F6D5;
    selection-color: #1B4332;
}}
QLineEdit:focus, QComboBox:focus {{
    border: 1.5px solid {_CLR_PRIMARY};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
    background: transparent;
}}
QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: #FFFFFF;
    color: #1B4332;
    border: 1.5px solid #A8D5BA;
    border-radius: 6px;
    padding: 4px;
    outline: none;
    selection-background-color: #C6F6D5;
    selection-color: #1B4332;
    font: 10pt 'Segoe UI';
}}
QComboBox QAbstractItemView::item {{
    padding: 6px 10px;
    min-height: 28px;
    color: #1B4332;
    background-color: #FFFFFF;
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: #EDF7F1;
    color: #1B4332;
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: #C6F6D5;
    color: #1B4332;
}}
QTableWidget {{
    background: #FFFFFF;
    border: 1.5px solid #A8D5BA;
    border-radius: 6px;
    gridline-color: #D6EDE0;
    font: 10pt 'Segoe UI';
    color: {_CLR_TEXT};
}}
QTableWidget::item {{
    padding: 6px 8px;
    color: {_CLR_TEXT};
}}
QTableWidget::item:selected {{
    background-color: #C6F6D5;
    color: {_CLR_TEXT};
}}
QHeaderView::section {{
    background-color: {_CLR_PRIMARY};
    color: #FFFFFF;
    padding: 7px;
    border: none;
    font: bold 9pt 'Segoe UI';
}}
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background: #C6F6D5;
    border-radius: 5px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover  {{ background: #A8D5BA; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""

_EDITOR_SS = """
QLineEdit {
    font: 10pt 'Segoe UI';
    padding: 5px 8px;
    border: 1.5px solid #2D6A4F;
    border-radius: 4px;
    background: #FFFFFF;
    color: #1B4332;
    min-height: 32px;
}
QLineEdit:focus { border-color: #1B4332; }
"""

_SAVE_BTN_SS = """
QPushButton {
    background-color: #2F6B3F;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 28px;
    font: bold 10pt 'Segoe UI';
    min-width: 100px;
}
QPushButton:hover   { background-color: #1B4332; }
QPushButton:pressed { background-color: #0D2B1A; }
"""

_CANCEL_BTN_SS = """
QPushButton {
    background-color: #FFFFFF;
    color: #2F6B3F;
    border: 1.5px solid #A8D5BA;
    border-radius: 8px;
    padding: 8px 28px;
    font: 10pt 'Segoe UI';
    min-width: 100px;
}
QPushButton:hover   { background-color: #F0FAF4; border-color: #2F6B3F; }
QPushButton:pressed { background-color: #C6F6D5; }
"""

_SECTION_LABEL_SS = """
QLabel {
    font: bold 10pt 'Segoe UI';
    color: #2F6B3F;
    background: transparent;
    padding: 2px 0px;
    letter-spacing: 0.3px;
}
"""

_FIELD_LABEL_SS = """
QLabel {
    font: 9pt 'Segoe UI';
    color: #4A6655;
    background: transparent;
    min-width: 90px;
}
"""


class _TallEditor(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setMinimumHeight(36)
        editor.setStyleSheet(_EDITOR_SS)
        return editor


def _hline():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: #D6EDE0;")
    line.setFixedHeight(1)
    return line


def _section_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(_SECTION_LABEL_SS)
    return lbl


class EditRecordDialog(QDialog):

    MONTHS   = [str(i) for i in range(1, 13)]
    DATES    = [str(i) for i in range(1, 32)]
    YEARS    = [str(i) for i in range(2015, 2030)]
    HOURS    = [f"{i}" for i in range(1, 13)]
    MINUTES  = [f"{i:02d}" for i in range(0, 60)]
    MERIDIEM = ["AM", "PM"]

    def __init__(self, record: dict, parent=None):
        super().__init__(parent)
        self.record = record
        self.setWindowTitle("Edit Record")
        self.setMinimumWidth(730)
        self.setMinimumHeight(780)
        self.setStyleSheet(_DIALOG_SS)
        self._build_ui()
        self._populate()

    # ── UI Build ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────────
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QWidget {
                background-color: #2F6B3F;
            }
        """)
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(20, 0, 20, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        h_title = QLabel("Edit Record Data")
        h_title.setStyleSheet(
            "font: bold 13pt 'Segoe UI'; color: #FFFFFF; background: transparent;")
        h_sub = QLabel("Update the fields below and press Save")
        h_sub.setStyleSheet(
            "font: 9pt 'Segoe UI'; color: rgba(255,255,255,0.70); background: transparent;")

        title_col.addWidget(h_title)
        title_col.addWidget(h_sub)
        h_lay.addLayout(title_col)
        h_lay.addStretch()
        root.addWidget(header)

        # ── Scrollable body ───────────────────────────────────────────────────
        from PyQt5.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea { background-color: #F0FAF4; border: none; }
            QScrollBar:vertical {
                background: transparent; width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #C6F6D5; border-radius: 5px; min-height: 24px;
            }
            QScrollBar::handle:vertical:hover { background: #A8D5BA; }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height: 0; }
        """)

        body = QWidget()
        body.setStyleSheet("background-color: #F0FAF4;")
        body_lay = QVBoxLayout(body)
        body_lay.setContentsMargins(24, 20, 24, 20)
        body_lay.setSpacing(10)

        # ── Client ────────────────────────────────────────────────────────────
        body_lay.addWidget(_section_label("Client Information"))
        body_lay.addWidget(_hline())

        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Enter client name…")
        self.client_input.setMinimumHeight(36)
        body_lay.addWidget(self._field_row("Client Name", self.client_input))
        body_lay.addSpacing(6)

        # ── Date & Time ───────────────────────────────────────────────────────
        body_lay.addWidget(_section_label("Date & Time"))
        body_lay.addWidget(_hline())
        body_lay.addWidget(self._field_row("Date", self._make_date_row()))
        body_lay.addSpacing(4)
        body_lay.addWidget(self._field_row("Time", self._make_time_row()))
        body_lay.addSpacing(6)

        # ── Chemicals Used ────────────────────────────────────────────────────
        body_lay.addWidget(_section_label("Chemicals Used"))
        body_lay.addWidget(_hline())
        self.chem_table = self._build_chem_table()
        body_lay.addWidget(self.chem_table)
        body_lay.addSpacing(10)

        # ── Actual Chemicals ──────────────────────────────────────────────────
        body_lay.addWidget(_section_label("Actual Chemicals on Hand"))
        body_lay.addWidget(_hline())
        self.actual_table = self._build_chem_table()
        body_lay.addWidget(self.actual_table)

        scroll.setWidget(body)
        root.addWidget(scroll)

        # ── Footer ────────────────────────────────────────────────────────────
        footer = QWidget()
        footer.setFixedHeight(64)
        footer.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-top: 1px solid #D6EDE0;
            }
        """)
        f_lay = QHBoxLayout(footer)
        f_lay.setContentsMargins(24, 0, 24, 0)
        f_lay.setSpacing(12)
        f_lay.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet(_CANCEL_BTN_SS)
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("Save Changes")
        self.btn_save.setStyleSheet(_SAVE_BTN_SS)
        self.btn_save.setFixedHeight(40)
        self.btn_save.setDefault(True)
        self.btn_save.clicked.connect(self._on_save)

        f_lay.addWidget(self.btn_cancel)
        f_lay.addWidget(self.btn_save)
        root.addWidget(footer)

    def _make_client_row(self):
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Enter client name…")
        return self.client_input

    def _make_date_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        self.month_cb = self._combo(self.MONTHS)
        self.date_cb  = self._combo(self.DATES)
        self.year_cb  = self._combo(self.YEARS)

        for cb, lbl in [(self.month_cb, "Month"), (self.date_cb, "Day"), (self.year_cb, "Year")]:
            l = QLabel(lbl)
            l.setStyleSheet(_FIELD_LABEL_SS + "min-width: 36px;")
            lay.addWidget(l)
            lay.addWidget(cb)
            if lbl != "Year":
                sep = QFrame()
                sep.setFrameShape(QFrame.VLine)
                sep.setStyleSheet("color: #D6EDE0;")
                lay.addWidget(sep)
        lay.addStretch()
        return row

    def _make_time_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        self.start_h        = self._combo(self.HOURS)
        self.start_m        = self._combo(self.MINUTES)
        self.start_meridiem = self._combo(self.MERIDIEM)
        self.end_h          = self._combo(self.HOURS)
        self.end_m          = self._combo(self.MINUTES)
        self.end_meridiem   = self._combo(self.MERIDIEM)

        def tag(text, bold=False):
            l = QLabel(text)
            style = "font: bold 9pt 'Segoe UI';" if bold else "font: 9pt 'Segoe UI';"
            l.setStyleSheet(f"background: transparent; color: #2F6B3F; {style}")
            return l

        lay.addWidget(tag("[S]", bold=True))
        lay.addWidget(self.start_h)
        lay.addWidget(tag(":"))
        lay.addWidget(self.start_m)
        lay.addWidget(self.start_meridiem)
        lay.addSpacing(10)

        arrow = QLabel("→")
        arrow.setStyleSheet("font: 12pt 'Segoe UI'; color: #A8D5BA; background: transparent;")
        lay.addWidget(arrow)
        lay.addSpacing(10)

        lay.addWidget(tag("[E]", bold=True))
        lay.addWidget(self.end_h)
        lay.addWidget(tag(":"))
        lay.addWidget(self.end_m)
        lay.addWidget(self.end_meridiem)
        lay.addStretch()
        return row

    def _field_row(self, label_text: str, widget: QWidget) -> QWidget:
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(12)

        lbl = QLabel(label_text)
        lbl.setStyleSheet(_FIELD_LABEL_SS)
        lbl.setFixedWidth(90)
        lay.addWidget(lbl)
        lay.addWidget(widget)
        return row

    def _combo(self, items):
        cb = QComboBox()
        cb.addItems(items)
        cb.setMinimumWidth(70)
        cb.setStyleSheet("""
            QComboBox {
                background: #FFFFFF;
                border-radius: 6px;
                padding: 4px 10px;
                font: 10pt 'Segoe UI';
                color: #1B4332;
                border: 1.5px solid #A8D5BA;
                min-height: 30px;
            }
            QComboBox:focus {
                border: 1.5px solid #2F6B3F;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background: transparent;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #1B4332;
                border: 1.5px solid #A8D5BA;
                border-radius: 4px;
                selection-background-color: #C6F6D5;
                selection-color: #1B4332;
                font: 10pt 'Segoe UI';
                outline: none;
            }
        """)
        # set directly on the view — this is the only reliable fix
        cb.view().setStyleSheet("""
            QListView {
                background-color: #FFFFFF;
                color: #1B4332;
                font: 10pt 'Segoe UI';
                border: none;
                outline: none;
                padding: 4px;
            }
            QListView::item {
                background-color: #FFFFFF;
                color: #1B4332;
                padding: 6px 10px;
                min-height: 28px;
            }
            QListView::item:hover {
                background-color: #EDF7F1;
                color: #1B4332;
            }
            QListView::item:selected {
                background-color: #C6F6D5;
                color: #1B4332;
            }
        """)
        return cb

    def _build_chem_table(self):
        t = QTableWidget(5, 3)
        t.setHorizontalHeaderLabels(["Chemical Name", "Quantity", "Remarks"])

        t.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        t.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        t.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        t.setColumnWidth(1, 100)

        t.setSelectionMode(QAbstractItemView.SingleSelection)
        t.setWordWrap(True)
        t.setShowGrid(True)
        t.setAlternatingRowColors(True)
        t.setStyleSheet("""
            QTableWidget {
                background: #FFFFFF;
                border: 1.5px solid #A8D5BA;
                border-radius: 8px;
                gridline-color: #D6EDE0;
                font: 10pt 'Segoe UI';
                color: #1B4332;
                alternate-background-color: #F0FAF4;
            }
            QTableWidget::item {
                padding: 6px 10px;
                color: #1B4332;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #C6F6D5;
                color: #1B4332;
            }
            QHeaderView::section {
                background-color: #2F6B3F;
                color: #FFFFFF;
                padding: 8px 10px;
                border: none;
                font: bold 9pt 'Segoe UI';
            }
            QScrollBar:vertical {
                background: transparent; width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #C6F6D5; border-radius: 4px; min-height: 20px;
            }
            QScrollBar::handle:vertical:hover { background: #A8D5BA; }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height: 0; }
        """)

        t.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        t.verticalHeader().setDefaultSectionSize(48)
        t.verticalHeader().setVisible(False)  # cleaner without row numbers

        t.setItemDelegate(_TallEditor(t))
        t.setMinimumHeight(290)
        t.setMaximumHeight(290)
        return t

    # ── Populate ──────────────────────────────────────────────────────────────

    def _populate(self):
        r = self.record
        chemicals_use    = r.get("chemicals_use")         or r.get("chemical_use")        or []
        actual_chemicals = r.get("actual_chemicals_used") or r.get("actual_chemical_used") or []

        self.client_input.setText(r.get("client_name", ""))

        self._set_combo(self.month_cb, str(r.get("month", "")))
        self._set_combo(self.date_cb,  str(r.get("date",  "")))
        self._set_combo(self.year_cb,  str(r.get("year",  "")))

        start = r.get("start_time", "01:00") or "01:00"
        end   = r.get("end_time",   "01:00") or "01:00"
        sh, sm = (start.split(":") + ["00"])[:2]
        eh, em = (end.split(":")   + ["00"])[:2]

        self._set_combo(self.start_h,        sh.lstrip("0") or "1")
        self._set_combo(self.start_m,        sm.zfill(2))
        self._set_combo(self.end_h,          eh.lstrip("0") or "1")
        self._set_combo(self.end_m,          em.zfill(2))
        self._set_combo(self.start_meridiem, r.get("start_meridiem", "AM"))
        self._set_combo(self.end_meridiem,   r.get("end_meridiem",   "AM"))

        self._fill_chem_table(self.chem_table,   chemicals_use)
        self._fill_chem_table(self.actual_table, actual_chemicals)

    def _set_combo(self, cb: QComboBox, value: str):
        idx = cb.findText(value.lstrip("0") or "0")
        if idx < 0:
            idx = cb.findText(value)
        if idx >= 0:
            cb.setCurrentIndex(idx)

    def _fill_chem_table(self, table: QTableWidget, chemicals: list):
        for row, entry in enumerate(chemicals[:5]):
            name = (
                entry.get("chemical_name") or
                entry.get("actual_chemicals_name") or
                entry.get("name") or ""
            )
            qty     = entry.get("quantity") or entry.get("qty") or ""
            remarks = entry.get("remarks") or ""

            for col, val in enumerate([name, qty, remarks]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                table.setItem(row, col, item)

    # ── Save ──────────────────────────────────────────────────────────────────

    def _on_save(self):
        client = self.client_input.text().strip()
        if not client:
            QMessageBox.warning(self, "Validation", "Client name is required.")
            return

        self.record["client_name"]        = client
        self.record["month"]              = int(self.month_cb.currentText())
        self.record["date"]               = int(self.date_cb.currentText())
        self.record["year"]               = int(self.year_cb.currentText())
        self.record["start_time"]         = f"{int(self.start_h.currentText()):02d}:{self.start_m.currentText()}"
        self.record["end_time"]           = f"{int(self.end_h.currentText()):02d}:{self.end_m.currentText()}"
        self.record["start_meridiem"]     = self.start_meridiem.currentText()
        self.record["end_meridiem"]       = self.end_meridiem.currentText()
        self.record["chemicals_use"]      = self._read_chem_table(self.chem_table,   "chemical_name")
        self.record["actual_chemicals_used"] = self._read_chem_table(self.actual_table, "actual_chemicals_name")

        self.accept()

    def _read_chem_table(self, table: QTableWidget, name_key: str) -> list:
        result = []
        for row in range(table.rowCount()):
            name = table.item(row, 0).text().strip() if table.item(row, 0) else ""
            qty  = table.item(row, 1).text().strip() if table.item(row, 1) else ""
            rem  = table.item(row, 2).text().strip() if table.item(row, 2) else ""
            if name:
                result.append({name_key: name, "quantity": qty, "remarks": rem})
        return result

    def get_data(self) -> dict:
        return self.record