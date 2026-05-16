from PyQt5.QtWidgets import QMainWindow
from ui.actual_chem_view import Ui_MainWindow
from util.live_update_delgate_viewer_util import LiveUpdateDelgate
from util.windows_viewer_util import ChemTableView, RowAction
from PyQt5.QtCore import pyqtSignal

class ActualChemViewerWindow(ChemTableView, QMainWindow):
    data_changed = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.delgate = LiveUpdateDelgate(self.ui.actualChemicalOnHand, self.emit_data)
        
        for col in range(3):
            self.ui.actualChemicalOnHand.setItemDelegateForColumn(col, self.delgate)
        
        self.ui.actualChemicalOnHand.itemChanged.connect(self.emit_data)
        
        self.ui.addRowBtn_chem.clicked.connect(lambda: self.operation_row(RowAction.ADD))
        self.ui.delRowBtn_chem.clicked.connect(lambda: self.operation_row(RowAction.DELETE))
        
    def _get_table(self):
        return self.ui.actualChemicalOnHand
     