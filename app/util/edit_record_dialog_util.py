from PyQt5.QtWidgets import (
    QTableWidgetItem, QWidget, QDialog,
    QHBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QLabel, QTableWidget,
    QVBoxLayout, QHeaderView, QAbstractItemView
)
from ui.style import edit_style

class EditRecordDialog(QDialog):
    
    MONTHS = [str(i) for i in range(1, 13)]
    DATES = [str(i) for i in range(1, 32)]
    YEARS = [str(i) for i in range(2015, 2030)]
    HOURS = [f"{i}" for i in range(1, 12)]
    MINUTES = [f"{i}" for i in range(0, 60)]
    MERIDIEM = ["AM", "PM"]
    
    def __init__(self, record: dict, parent=None):
        super().__init__(parent)
        self.record = record
        self.setWindowTitle("Edit Record Data")
        self.setMinimumWidth(520)
        self.setStyleSheet(edit_style)
        self._build_ui()
        self._populate()
        
    def _build_ui(self):
        root = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)
        root.addLayout(form)

        # Client name
        self.client_input = QLineEdit()
        form.addRow("Client Name:", self.client_input)

        # Date row
        date_row = QWidget(); dl = QHBoxLayout(date_row); dl.setContentsMargins(0,0,0,0)
        self.month_cb  = self._combo(self.MONTHS)
        self.date_cb   = self._combo(self.DATES)
        self.year_cb   = self._combo(self.YEARS)
        for w, lbl in [(self.month_cb,"Mo"),(self.date_cb,"Dy"),(self.year_cb,"Yr")]:
            dl.addWidget(QLabel(lbl)); dl.addWidget(w)
        form.addRow("Date:", date_row)

        # Time row
        time_row = QWidget(); tl = QHBoxLayout(time_row); tl.setContentsMargins(0,0,0,0)
        self.start_h   = self._combo(self.HOURS)
        self.start_m   = self._combo(self.MINUTES)
        self.end_h     = self._combo(self.HOURS)
        self.end_m     = self._combo(self.MINUTES)
        self.meridiem  = self._combo(self.MERIDIEM)
        for w, lbl in [(self.start_h,"Start H"),(self.start_m,"M"),
                       (self.end_h,"  End H"),(self.end_m,"M"),(self.meridiem,"")]:
            if lbl: tl.addWidget(QLabel(lbl))
            tl.addWidget(w)
        form.addRow("Time:", time_row)

        # Remarks
        self.remarks_input = QLineEdit()
        form.addRow("Remarks:", self.remarks_input)

        # Chemical tables
        root.addWidget(QLabel("Chemicals Used:"))
        self.chem_table = self._build_chem_table()
        root.addWidget(self.chem_table)

        root.addWidget(QLabel("Actual Chemicals on Hand:"))
        self.actual_table = self._build_chem_table()
        root.addWidget(self.actual_table)

        # OK / Cancel
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._on_save)
        btns.rejected.connect(self.reject)
        root.addWidget(btns)

    def _combo(self, items):
        cb = QComboBox()
        cb.addItems(items)
        return cb

    def _build_chem_table(self):
        t = QTableWidget(5, 3)
        t.setHorizontalHeaderLabels(["Chemical Name", "Quantity", "Remarks"])
        t.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        t.setSelectionMode(QAbstractItemView.SingleSelection)
        t.verticalHeader().setDefaultSectionSize(32)
        t.setFixedHeight(190)
        return t

    # ── Populate ──────────────────────────────────────────────────────────────

    def _populate(self):
        r = self.record
        self.client_input.setText(r.get("client_name", ""))
        self.remarks_input.setText(r.get("remarks", "") or "")

        self._set_combo(self.month_cb,  str(r.get("month", "")))
        self._set_combo(self.date_cb,   str(r.get("date",  "")))
        self._set_combo(self.year_cb,   str(r.get("year",  "")))

        start = r.get("start_time", "01:00") or "01:00"
        end   = r.get("end_time",   "01:00") or "01:00"
        sh, sm = (start.split(":") + ["00"])[:2]
        eh, em = (end.split(":")   + ["00"])[:2]

        self._set_combo(self.start_h,  sh.zfill(2))
        self._set_combo(self.start_m,  sm.zfill(2))
        self._set_combo(self.end_h,    eh.zfill(2))
        self._set_combo(self.end_m,    em.zfill(2))
        self._set_combo(self.meridiem, r.get("meridiem", "AM"))

        self._fill_chem_table(self.chem_table,   r.get("chemicals_use", []))
        self._fill_chem_table(self.actual_table, r.get("actual_chemicals_used", []))

    def _set_combo(self, cb: QComboBox, value: str):
        idx = cb.findText(value.lstrip("0") or "0")
        if idx < 0:
            idx = cb.findText(value)
        if idx >= 0:
            cb.setCurrentIndex(idx)

    def _fill_chem_table(self, table: QTableWidget, chemicals: list):
        for row, entry in enumerate(chemicals[:5]):
            key = "chemical_name" if "chemical_name" in entry else "name"
            table.setItem(row, 0, QTableWidgetItem(entry.get(key, "")))
            table.setItem(row, 1, QTableWidgetItem(entry.get("quantity", entry.get("qty", ""))))
            table.setItem(row, 2, QTableWidgetItem(entry.get("remarks", "")))

    # ── Save ──────────────────────────────────────────────────────────────────

    def _on_save(self):
        client = self.client_input.text().strip()
        if not client:
            QMessageBox.warning(self, "Validation", "Client name is required.")
            return

        self.record["client_name"] = client
        self.record["remarks"]     = self.remarks_input.text().strip()
        self.record["month"]       = int(self.month_cb.currentText())
        self.record["date"]        = int(self.date_cb.currentText())
        self.record["year"]        = int(self.year_cb.currentText())
        self.record["start_time"]  = f"{self.start_h.currentText()}:{self.start_m.currentText()}"
        self.record["end_time"]    = f"{self.end_h.currentText()}:{self.end_m.currentText()}"
        self.record["meridiem"]    = self.meridiem.currentText()
        self.record["chemicals_use"]          = self._read_chem_table(self.chem_table,   "chemical_name")
        self.record["actual_chemicals_used"]  = self._read_chem_table(self.actual_table, "chemical_name")

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