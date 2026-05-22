# login/login.py
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore    import pyqtSignal
from PyQt5.QtGui     import QIcon
from ui.login        import Ui_Login
from .register_dialog       import RegisterDialog
from .forgot_password_dialog import ForgotPasswordDialog
import os

from service.offline.Database.localDatabase import session_local
from service.offline.Repositories.localRepository import local_admin_repo
from passlib.context import CryptContext

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH  = os.path.join(os.path.dirname(CURRENT_DIR), "ui", "assets")


class LoginService:
    def __init__(self, ui, api_service, parent_window):
        self.ui             = ui
        self.api            = api_service
        self.parent_window  = parent_window

    def attempt_login(self):
        user     = self.ui.usernameEdit.text().strip()
        password = self.ui.passwordEdit.text()
 
        if not user or not password:
           
            QMessageBox.warning(self.parent_window, "Input Error",
                                "Please enter both username and password.")
            return
 
        success, msg = self.api.login_service(user, password)
        if success:
            self.api.admin_under = user
 
            # ── Cache credentials for offline login ───────────────────────────
            # Only possible if we're online (login just succeeded against MySQL)
            try:
 
                _pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
                hashed = _pwd.hash(password)           # hash the plain password
 
                db = session_local()
                try:
                    local_admin_repo.upsert(
                        db,
                        username      = user,
                        password_hash = hashed,
                        role          = "admin",
                        email         = None,          # fetched separately if needed
                    )
                finally:
                    db.close()
            except Exception as e:
                print(f"[LoginService] Could not cache credentials: {e}")
            # ─────────────────────────────────────────────────────────────────
 
            self.parent_window.login_success.emit()
        else:
            if "429" in str(msg) or "Too Many Request" in str(msg):
                self.ui.loginbutton.setEnabled(False)
                QMessageBox.critical(self.parent_window, "Locked",
                                     "Too many requests. Try again in 60 s.") 
            QMessageBox.warning(self.parent_window, "Login Failed", f"Error: {msg}")
            self.ui.passwordEdit.clear()
            self.ui.passwordEdit.setFocus()
 


class LoginWindow(QMainWindow):
    login_success = pyqtSignal()

    def __init__(self, api_service):
        super().__init__()
        self.ui  = Ui_Login()
        self.ui.setupUi(self)
        self.api = api_service

        self.login_service = LoginService(self.ui, api_service, self)
        self.setWindowIcon(QIcon(f"{IMAGE_PATH}/Logo.png"))

        # Existing wiring
        self.ui.usernameEdit.returnPressed.connect(self.ui.passwordEdit.setFocus)
        self.ui.passwordEdit.returnPressed.connect(self.login_service.attempt_login)
        self.ui.loginbutton.clicked.connect(self.login_service.attempt_login)

        # New button wiring
        self.ui.registerBtn.clicked.connect(self._open_register)
        self.ui.forgotBtn.clicked.connect(self._open_forgot_password)

    # ── Dialog launchers ──────────────────────────────────────────────────────

    def _open_register(self):
        dlg = RegisterDialog(self.api, parent=self)
        dlg.exec_()

    def _open_forgot_password(self):
        dlg = ForgotPasswordDialog(self.api, parent=self)
        dlg.exec_()