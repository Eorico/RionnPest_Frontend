from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ui.login import Ui_Login

from PyQt5.QtGui import QIcon
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(os.path.dirname(CURRENT_DIR), "ui", "assets")

class LoginService:
    def __init__(self, ui, api_service, parent_window):
        self.ui = ui
        self.api = api_service
        self.parent_window = parent_window
        
    def attempt_login(self):
        user = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()
        
        if not user or not password:
            QMessageBox.warning(self.parent_window, "Input Error", "Please enter both username and password.")
            return
        
        success, msg = self.api.login_service(user, password)
        if success:
            self.api.admin_under = user
            print(f"Login successful for user: {user}")
            self.parent_window.login_success.emit()
        else:
            if "429" in str(msg) or "Too Many Request" in str(msg):
                self.ui.loginbutton.setEnabled(False)
                QMessageBox.critical(self.parent_window, "locked", "Too many requests. Try again in 60s")
                
            QMessageBox.warning(self.parent_window, "Login Failed", f"Error: {msg}")
            self.ui.passwordEdit.clear()
            self.ui.passwordEdit.setFocus()

class LoginWindow(QMainWindow):
    login_success = pyqtSignal()
    
    def __init__(self, api_service):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.api = api_service
        
        self.login_service = LoginService(self.ui, api_service, self)
        
        self.setWindowIcon(QIcon(f"{IMAGE_PATH}/Logo.png"))
        
        self.ui.usernameEdit.returnPressed.connect(self.ui.passwordEdit.setFocus)
        self.ui.passwordEdit.returnPressed.connect(self.login_service.attempt_login)
        
        self.ui.loginbutton.clicked.connect(self.login_service.attempt_login)
        
        