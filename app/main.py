from PyQt5.QtWidgets import QApplication
from service.api.api_service import ApiService
from intro.intro import IntroWindow
from login.login import LoginWindow
from dashboard.dashboard import DashboardWindow
from service.connections.syncEngine import SyncManager
from recycle.recycle_bin import RecyclBinWindow
from dashboard.viewer.actual_chemical_viewer import ActualChemViewerWindow
from dashboard.viewer.chemical_used_viewer import ChemUseViewerWindow
from docs_viewer.docs_viewer import DocsViewerWindow
import sys

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.api = ApiService()

        self.sync_manager = SyncManager(self.api)
        
        self.intro = IntroWindow(self.sync_manager, self.api)
        self.login = LoginWindow(self.api)
        self.dashboard = DashboardWindow(self.api)
        self.recycle_bin = RecyclBinWindow(self.api, self.dashboard.load_table_data_dashboard, parent=self.dashboard)
        self.docs_viewer = DocsViewerWindow(self.api)
        
        self.actual_chem_viewer = ActualChemViewerWindow()
        self.chem_use_viewer = ChemUseViewerWindow()
        
        self.intro.intro_service.finished.connect(self.show_login)
        self.login.login_success.connect(self.show_dashboard)
        self.dashboard.ui.recycle_bin.triggered.connect(self.show_recycle_bin)
        self.dashboard.ui.ViewChem.clicked.connect(self.show_chem_use_viewer)
        self.dashboard.ui.ViewActChem.clicked.connect(self.show_actual_chem_viewer)
        self.dashboard.ui.actionPDF_STORAGE.triggered.connect(self.show_docs_viewer)
        
        self.chem_use_viewer.data_changed.connect(
            lambda data: self.dashboard.update_table_inputs_dashboard(self.dashboard.ui.chemicalUsed ,data)
        )
        
        self.actual_chem_viewer.data_changed.connect(
            lambda data: self.dashboard.update_table_inputs_dashboard(self.dashboard.ui.actualchemicalUsed ,data)
        )
        
        self.dashboard.ui.chemicalUsed.itemChanged.connect(
            lambda: self._sync_dashboard_to_viewer(
                self.dashboard.ui.chemicalUsed,
                self.chem_use_viewer
            )
        )
        self.dashboard.ui.actualchemicalUsed.itemChanged.connect(
            lambda: self._sync_dashboard_to_viewer(
                self.dashboard.ui.actualchemicalUsed,
                self.actual_chem_viewer
            )
        )
        
        self.intro.show()
        
    def show_login(self):
        self.intro.close()
        self.login.show()
        
    def show_dashboard(self):
        self.login.close()
        self.dashboard.load_table_data_dashboard()
        self.dashboard.show()
        
    def show_recycle_bin(self):
        self.recycle_bin.load_bin_data_restore()
        self.recycle_bin.show()
        
    def show_docs_viewer(self):
        self.docs_viewer.show()

    def show_actual_chem_viewer(self):
        self.actual_chem_viewer.show()
    
    def show_chem_use_viewer(self):
        self.chem_use_viewer.show()
        
    def _sync_dashboard_to_viewer(self, source_table, viewer_window):
        data = []
        for row in range(source_table.rowCount()):
            name = source_table.item(row, 0).text().strip() if source_table.item(row, 0) else ""
            qty = source_table.item(row, 1).text().strip() if source_table.item(row, 1) else ""
            remarks = source_table.item(row, 2).text().strip() if source_table.item(row, 2) else ""
            if name or qty or remarks:
                data.append({"name": name, "qty": qty, "remarks": remarks})

        viewer_window.load_data(data)
    
if __name__ == "__main__":
    manager = MainApp()
    sys.exit(manager.app.exec_())