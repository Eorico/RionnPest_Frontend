from PyQt5.QtWidgets import QApplication
from service.api.api_service import ApiService
from intro.intro import IntroWindow
from login.login import LoginWindow
from dashboard.dashboard import DashboardWindow
from service.connections.syncEngine import SyncManager
from recycle.recycle_bin import RecyclBinWindow
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
        
        self.intro.finished.connect(self.show_login)
        self.login.login_success.connect(self.show_dashboard)
        self.dashboard.ui.RecycleBin_btn.clicked.connect(self.show_recycle_bin)
        
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
    
if __name__ == "__main__":
    manager = MainApp()
    sys.exit(manager.app.exec_())