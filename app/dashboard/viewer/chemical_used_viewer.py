from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from util.live_update_delgate_viewer_util import LiveUpdateDelgate
from util.windows_viewer_util import ChemTableView, RowAction
from ui.chem_use__view import Ui_MainWindow

class ChemUseViewerWindow(ChemTableView, QMainWindow):
    data_changed = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.delgate = LiveUpdateDelgate(self.ui.chemicalUsed, self.emit_data)
        
        for col in range(3):
            self.ui.chemicalUsed.setItemDelegateForColumn(col, self.delgate)
        
        self.ui.chemicalUsed.itemChanged.connect(self.emit_data)
        
        self.ui.addRowBtn_chem.clicked.connect(lambda: self.operation_row(RowAction.ADD))
        self.ui.delRowBtn_chem.clicked.connect(lambda: self.operation_row(RowAction.DELETE))
        
    def _get_table(self):
        return self.ui.chemicalUsed