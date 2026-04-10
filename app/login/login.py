from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ui.login import Ui_Login

class LoginWindow(QMainWindow):
    login_success = pyqtSignal()
    
    def __init__(self, api_service):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.api = api_service
        
        self.ui.usernameEdit.returnPressed.connect(self.ui.passwordEdit.setFocus)
        self.ui.passwordEdit.returnPressed.connect(self.attempt_login)
        
        self.ui.loginbutton.clicked.connect(self.attempt_login)
        
    def attempt_login(self):
        user = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()
        
        if not user or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return
        
        success, msg = self.api.login_service(user, password)
        if success:
            self.api.admin_under = user
            print(f"Login successful for user: {user}")
            self.login_success.emit()
        else:
            if "429" in str(msg) or "Too Many Request" in str(msg):
                self.ui.loginbutton.setEnabled(False)
                QMessageBox.critical(self, "locked", "Too many requests. Try again in 60s")
                
            QMessageBox.warning(self, "Login Failed", f"Error: {msg}")
            self.ui.passwordEdit.clear()
            self.ui.passwordEdit.setFocus()