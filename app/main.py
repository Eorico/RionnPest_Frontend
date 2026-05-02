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
        self.recycle_bin = RecyclBinWindow(
            self.api, 
            self.dashboard.load_table_data_dashboard, 
            parent=self.dashboard
        )
        
        self.docs_viewer = DocsViewerWindow(self.api)
        self.actual_chem_viewer = ActualChemViewerWindow()
        self.chem_use_viewer = ChemUseViewerWindow()
        
        self._bind_viewer(
            viewer=self.chem_use_viewer,
            dashboard_table=self.dashboard.ui.chemicalUsed
        )
        
        self._bind_viewer(
            viewer=self.actual_chem_viewer,
            dashboard_table=self.dashboard.ui.actualchemicalUsed
        )
        
        self.intro.intro_service.finished.connect(self.show_login)
        self.login.login_success.connect(self.show_dashboard)
        self.dashboard.ui.recycle_bin.triggered.connect(self.recycle_bin.show)
        self.dashboard.ui.ViewChem.clicked.connect(self.chem_use_viewer.show)
        self.dashboard.ui.actionPDF_STORAGE_3.triggered.connect(self.docs_viewer.show)
        self.dashboard.ui.ViewActChem.clicked.connect(self.actual_chem_viewer.show)
        
        self.intro.show()
        
    def _bind_viewer(self, viewer, dashboard_table):
        
        viewer.data_changed.connect(
            lambda data: self.dashboard.update_table_inputs_dashboard(dashboard_table, data)
        )
        
        dashboard_table.itemChanged.connect(
            lambda: self._sync_table_to_viewer(dashboard_table, viewer)
        )
        
    def _sync_table_to_viewer(self, source_table, viewer):
        data = []
        for row in range(source_table.rowCount()):
            name = source_table.item(row, 0).text().strip() if source_table.item(row, 0) else ""
            qty = source_table.item(row, 1).text().strip() if source_table.item(row, 1) else ""
            remarks = source_table.item(row, 2).text().strip() if source_table.item(row, 2) else ""
            
            if name or qty or remarks:
                data.append({
                    "name": name,
                    "qty": qty,
                    "remarks": remarks
                })
        viewer.load_data(data)
            
    def show_login(self):
        self.intro.close()
        self.login.show()
        
    def show_dashboard(self):
        self.login.close()
        self.dashboard.load_table_data_dashboard()
        self.dashboard.show()
        
    
if __name__ == "__main__":
    manager = MainApp()
    sys.exit(manager.app.exec_())