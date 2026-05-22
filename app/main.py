from PyQt5.QtWidgets import QApplication
from service.api.api_service import ApiService
from service.offline.Service.offlineApiService import OfflineCapableApiService  # ← NEW
from service.offline.Database.localDatabase import init_db                       # ← NEW
from util.toolfix_util import install_custom_tooltips
import sys

from intro.intro import IntroWindow
from login.login import LoginWindow
from dashboard.dashboard import DashboardWindow
from service.connections.syncEngine import SyncManager
from recycle.recycle_bin import RecyclBinWindow
from dashboard.viewer.actual_chemical_viewer import ActualChemViewerWindow
from dashboard.viewer.chemical_used_viewer import ChemUseViewerWindow


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        install_custom_tooltips(self.app)

        # ── Init SQLite tables (creates local_database.db if not exists) ──────
        init_db()

        # ── Wrap ApiService with offline capability ───────────────────────────
        _online_api  = ApiService()                        # real MySQL/FastAPI
        self.api     = OfflineCapableApiService(_online_api)  # offline-aware wrapper
        self.sync_manager = SyncManager(_online_api)       # uses real api for syncing

        self.intro     = IntroWindow(self.sync_manager, self.api)
        self.login     = LoginWindow(self.api)
        self.dashboard = DashboardWindow(self.api)
        self.recycle_bin = RecyclBinWindow(
            self.api,
            self.dashboard.load_table_data_dashboard,
            parent=self.dashboard
        )

        self.actual_chem_viewer = ActualChemViewerWindow()
        self.chem_use_viewer    = ChemUseViewerWindow()

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
        self.dashboard.ui.recycle_bin.clicked.connect(self.recycle_bin.show)
        self.dashboard.ui.ViewChem.clicked.connect(self.chem_use_viewer.show)
        self.dashboard.ui.ViewActChem.clicked.connect(self.actual_chem_viewer.show)

        self.dashboard.ui.actionPDF_STORAGE.triggered.connect(
            self.dashboard.open_docx_viewer)
        self.dashboard.ui.actionPDF_STORAGE_3.clicked.connect(
            self.dashboard.open_docx_viewer)

        self.intro.show()

        self.dashboard.logged_out.connect(self.return_to_login)
        self.dashboard.record_saved.connect(self._on_record_saved)

    def _bind_viewer(self, viewer, dashboard_table):
        viewer.data_changed.connect(
            lambda data: self.dashboard.update_table_inputs_dashboard(
                dashboard_table, data)
        )

    def _sync_table_to_viewer(self, source_table, viewer):
        data = []
        for row in range(source_table.rowCount()):
            name    = source_table.item(row, 0).text().strip() if source_table.item(row, 0) else ""
            qty     = source_table.item(row, 1).text().strip() if source_table.item(row, 1) else ""
            remarks = source_table.item(row, 2).text().strip() if source_table.item(row, 2) else ""
            if name or qty or remarks:
                data.append({"name": name, "qty": qty, "remarks": remarks})
        viewer.load_data(data)

    def show_login(self):
        self.intro.close()
        # Sync any offline records now that we know connectivity status
        if self.api.check_connection_service():
            ok, msg = self.sync_manager.sync_pending_records()
            print(f"[Sync on startup] {msg}")
        self.login.show()

    def show_dashboard(self):
        self.login.close()
        # Sync after login while token is fresh
        if self.api.check_connection_service():
            ok, msg = self.sync_manager.sync_pending_records()
            print(f"[Sync after login] {msg}")
        self.dashboard.load_table_data_dashboard()
        self.dashboard.show()

    def return_to_login(self):
        self.dashboard.hide()
        self.dashboard.clear_inputs_dashboard()
        self.dashboard.table_renderer.clear()
        self.api.logout_service()
        self.login.ui.usernameEdit.clear()
        self.login.ui.passwordEdit.clear()
        self.login.show()

    def _on_record_saved(self):
        self.chem_use_viewer.clear_table()
        self.actual_chem_viewer.clear_table()


if __name__ == "__main__":
    manager = MainApp()
    sys.exit(manager.app.exec_())