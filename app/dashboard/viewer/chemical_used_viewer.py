from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from util.live_update_delgate_viewer_util import LiveUpdateDelgate
from ui.chem_use__view import Ui_MainWindow

class ChemUseViewerWindow(QMainWindow):
    data_changed = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.delgate = LiveUpdateDelgate(self.ui.chemicalUsed, self.emit_data_chem_use)
        
        for col in range(3):
            self.ui.chemicalUsed.setItemDelegateForColumn(col, self.delgate)
        
        self.ui.chemicalUsed.itemChanged.connect(self.emit_data_chem_use)
        
    def emit_data_chem_use(self):
        chemical_list = []
        table = self.ui.chemicalUsed
        for row in range(table.rowCount()):
            name = table.item(row, 0).text().strip() if table.item(row, 0) else ""
            qty = table.item(row, 1).text().strip() if table.item(row, 1) else ""  
            remarks = table.item(row, 2).text().strip() if table.item(row, 2) else ""
            
            if name or qty or remarks:
                chemical_list.append({
                    "name": name,
                    "qty": qty,
                    "remarks": remarks
            })

        self.data_changed.emit(chemical_list)
        
    def load_data(self, data: list):
        table = self.ui.chemicalUsed
        table.blockSignals(True)
        for row in range(table.rowCount()):
            entry = data[row] if row < len(data) else {}

            table.setItem(row, 0, QTableWidgetItem(entry.get("name", "")))
            table.setItem(row, 1, QTableWidgetItem(entry.get("qty", "")))
            table.setItem(row, 2, QTableWidgetItem(entry.get("remarks", "")))

        table.blockSignals(False)