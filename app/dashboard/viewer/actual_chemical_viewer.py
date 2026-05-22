from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from ui.actual_chem_view import Ui_MainWindow
from util.live_update_delgate_viewer_util import LiveUpdateDelgate
from util.windows_viewer_util import ChemTableView, RowAction
from PyQt5.QtCore import pyqtSignal

DEFAULT_ROWS = 5


class ActualChemViewerWindow(ChemTableView, QMainWindow):
    data_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._undo_stack: list[list[list[str]]] = []   # stack of table snapshots

        self.delgate = LiveUpdateDelgate(self.ui.actualChemicalOnHand, self.emit_data)
        for col in range(3):
            self.ui.actualChemicalOnHand.setItemDelegateForColumn(col, self.delgate)

        # Snapshot on cell edits
        self.ui.actualChemicalOnHand.itemChanged.connect(self._on_item_changed)

        # Add / Delete rows — snapshot first, then mutate
        self.ui.addRowBtn_chem.clicked.connect(self._add_row)
        self.ui.delRowBtn_chem.clicked.connect(self._delete_row)

        # Undo / Done
        self.ui.undoBtn.clicked.connect(self._undo)
        self.ui.doneBtn.clicked.connect(self.close)

        self._update_undo_btn()

    # ── Public API ────────────────────────────────────────────────────────────

    def clear_table(self):
        """Called by MainApp after a record is successfully saved."""
        self._push_snapshot()
        tbl = self.ui.actualChemicalOnHand
        tbl.blockSignals(True)
        tbl.setRowCount(DEFAULT_ROWS)
        for r in range(DEFAULT_ROWS):
            for c in range(tbl.columnCount()):
                tbl.setItem(r, c, QTableWidgetItem(""))
            tbl.setVerticalHeaderItem(r, QTableWidgetItem(str(r + 1)))
        tbl.blockSignals(False)
        self.emit_data()
        self._update_undo_btn()

    def load_data(self, data: list):
        """Populate table from a list of {name, qty, remarks} dicts."""
        self._push_snapshot()
        tbl = self.ui.actualChemicalOnHand
        tbl.blockSignals(True)
        rows = max(DEFAULT_ROWS, len(data))
        tbl.setRowCount(rows)
        for r, entry in enumerate(data):
            tbl.setItem(r, 0, QTableWidgetItem(entry.get("name", "")))
            tbl.setItem(r, 1, QTableWidgetItem(entry.get("qty", "")))
            tbl.setItem(r, 2, QTableWidgetItem(entry.get("remarks", "")))
        for r in range(len(data), rows):
            for c in range(tbl.columnCount()):
                tbl.setItem(r, c, QTableWidgetItem(""))
        tbl.blockSignals(False)
        self.emit_data()
        self._update_undo_btn()

    # ── Row operations ────────────────────────────────────────────────────────

    def _add_row(self):
        self._push_snapshot()
        self.operation_row(RowAction.ADD)
        self._update_undo_btn()

    def _delete_row(self):
        tbl = self.ui.actualChemicalOnHand
        if tbl.rowCount() == 0:
            return
        self._push_snapshot()
        self.operation_row(RowAction.DELETE)
        self._update_undo_btn()

    # ── Undo ─────────────────────────────────────────────────────────────────

    def _on_item_changed(self):
        current = self._snapshot()
        if not self._undo_stack or self._undo_stack[-1] != current:
            self._undo_stack.append(current)
        self.emit_data()
        self._update_undo_btn()

    def _push_snapshot(self):
        self._undo_stack.append(self._snapshot())

    def _snapshot(self) -> list[list[str]]:
        tbl = self.ui.actualChemicalOnHand
        state = []
        for r in range(tbl.rowCount()):
            row = []
            for c in range(tbl.columnCount()):
                item = tbl.item(r, c)
                row.append(item.text() if item else "")
            state.append(row)
        return state

    def _undo(self):
        if not self._undo_stack:
            return
        state = self._undo_stack.pop()
        tbl = self.ui.actualChemicalOnHand
        tbl.blockSignals(True)
        tbl.setRowCount(len(state))
        for r, row in enumerate(state):
            for c, val in enumerate(row):
                tbl.setItem(r, c, QTableWidgetItem(val))
            tbl.setVerticalHeaderItem(r, QTableWidgetItem(str(r + 1)))
        tbl.blockSignals(False)
        self.emit_data()
        self._update_undo_btn()

    def _update_undo_btn(self):
        self.ui.undoBtn.setEnabled(bool(self._undo_stack))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_table(self):
        return self.ui.actualChemicalOnHand