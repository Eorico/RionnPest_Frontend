# login/register_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QCursor

_G400 = "#2D6A4F"
_G600 = "#1B4332"
_G100 = "#C6F6D5"
_BG   = "#F8FBF9"
_BORDER = "#D4E6DA"

_INPUT_SS = """
QLineEdit {
    background: #fff; color: #1B4332; border: 1.5px solid #D4E6DA;
    border-radius: 8px; padding: 10px 14px; font: 11pt 'Segoe UI';
}
QLineEdit:focus { border: 2px solid #2D6A4F; }
QLineEdit:hover { border-color: #74C69D; background: #F4FBF7; }
"""
_BTN_SS = f"""
QPushButton {{
    background: {_G400}; color: #fff; border: none;
    border-radius: 8px; font: bold 10pt 'Segoe UI';
    letter-spacing: 2px; padding: 12px;
}}
QPushButton:hover   {{ background: {_G600}; }}
QPushButton:pressed {{ background: #081C15; }}
QPushButton:disabled {{ background: #B7D5C4; color: rgba(255,255,255,0.6); }}
"""
_LINK_SS = f"""
QPushButton {{ background: transparent; border: none;
    color: {_G400}; font: 9pt 'Segoe UI'; text-decoration: underline; }}
QPushButton:hover {{ color: {_G600}; }}
"""
_LBL_SS = f"""
QLabel {{ background: transparent; border: none; color: {_G400};
    font: bold 8pt 'Segoe UI'; letter-spacing: 2px; }}
"""
_ERR_SS = "QLabel { color: #DC2626; font: 9pt 'Segoe UI'; background: transparent; }"
_OK_SS  = f"QLabel {{ color: {_G400}; font: 9pt 'Segoe UI'; background: transparent; }}"


class RegisterDialog(QDialog):
    def __init__(self, api_service, parent=None):
        super().__init__(parent)
        self.api   = api_service
        self._drag = None
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(420)
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)

        self._card = QFrame()
        self._card.setStyleSheet(f"""
            QFrame {{ background: {_BG}; border-radius: 16px;
                     border: 1px solid {_BORDER}; }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40); shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 70))
        self._card.setGraphicsEffect(shadow)
        outer.addWidget(self._card)

        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(40, 36, 40, 36)
        lay.setSpacing(0)

        # Header
        hdr = QHBoxLayout()
        title = QLabel("Create Account")
        title.setStyleSheet(f"color: {_G600}; font: bold 18pt 'Georgia'; background: transparent;")
        hdr.addWidget(title)
        hdr.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton { background: transparent; border: none;
                color: #A0B8AB; font: bold 10pt 'Segoe UI'; border-radius: 13px; }
            QPushButton:hover { background: #E8F5EE; color: #1B4332; }
        """)
        close_btn.clicked.connect(self.reject)
        hdr.addWidget(close_btn)
        lay.addLayout(hdr)
        lay.addSpacing(4)

        sub = QLabel("Fill in the details to register a new admin")
        sub.setStyleSheet("color: #6B8F78; font: 9pt 'Segoe UI'; background: transparent;")
        lay.addWidget(sub)
        lay.addSpacing(24)

        def _field(label_txt, placeholder, echo=False):
            lbl = QLabel(label_txt)
            lbl.setStyleSheet(_LBL_SS)
            lay.addWidget(lbl)
            lay.addSpacing(5)
            edit = QLineEdit()
            edit.setFixedHeight(44)
            edit.setPlaceholderText(placeholder)
            edit.setStyleSheet(_INPUT_SS)
            if echo:
                edit.setEchoMode(QLineEdit.Password)
            lay.addWidget(edit)
            lay.addSpacing(14)
            return edit

        self.usernameEdit = _field("USERNAME", "Choose a username")
        self.emailEdit    = _field("EMAIL", "your@gmail.com")
        self.passwordEdit = _field("PASSWORD", "At least 8 characters", echo=True)
        self.confirmEdit  = _field("CONFIRM PASSWORD", "Repeat password", echo=True)

        # ── Enter-key navigation between fields ───────────────────────────────
        self.usernameEdit.returnPressed.connect(self.emailEdit.setFocus)
        self.emailEdit.returnPressed.connect(self.passwordEdit.setFocus)
        self.passwordEdit.returnPressed.connect(self.confirmEdit.setFocus)
        self.confirmEdit.returnPressed.connect(self._attempt_register)

        self.statusLbl = QLabel("")
        self.statusLbl.setWordWrap(True)
        self.statusLbl.setStyleSheet(_ERR_SS)
        lay.addWidget(self.statusLbl)
        lay.addSpacing(6)

        self.registerBtn = QPushButton("CREATE ACCOUNT")
        self.registerBtn.setFixedHeight(46)
        self.registerBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.registerBtn.setStyleSheet(_BTN_SS)
        self.registerBtn.clicked.connect(self._attempt_register)
        lay.addWidget(self.registerBtn)
        lay.addSpacing(16)

        back_row = QHBoxLayout()
        back_row.addStretch()
        back_btn = QPushButton("Already have an account? Sign in")
        back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        back_btn.setStyleSheet(_LINK_SS)
        back_btn.clicked.connect(self.reject)
        back_row.addWidget(back_btn)
        back_row.addStretch()
        lay.addLayout(back_row)

        # ── Drag — use proper methods, NOT value-returning lambdas ────────────
        self._card.mousePressEvent   = self._drag_press
        self._card.mouseMoveEvent    = self._drag_move
        self._card.mouseReleaseEvent = self._drag_release

    # ── Drag handlers (return None — required by PyQt5) ───────────────────────
    def _drag_press(self, event):
        if event.button() == Qt.LeftButton:
            self._drag = event.globalPos()

    def _drag_move(self, event):
        if event.buttons() == Qt.LeftButton and self._drag is not None:
            self.move(self.pos() + event.globalPos() - self._drag)
            self._drag = event.globalPos()

    def _drag_release(self, event):
        self._drag = None

    # ── Register logic ────────────────────────────────────────────────────────
    def _attempt_register(self):
        username = self.usernameEdit.text().strip()
        email    = self.emailEdit.text().strip()
        password = self.passwordEdit.text()
        confirm  = self.confirmEdit.text()

        if not all([username, email, password, confirm]):
            self._err("All fields are required.")
            return
        if len(password) < 8:
            self._err("Password must be at least 8 characters.")
            return
        if password != confirm:
            self._err("Passwords do not match.")
            return
        if "@" not in email or "." not in email.split("@")[-1]:
            self._err("Enter a valid email address.")
            return

        self.registerBtn.setEnabled(False)
        self.registerBtn.setText("Creating…")

        success, msg = self.api.register_service(username, password, email)

        self.registerBtn.setEnabled(True)
        self.registerBtn.setText("CREATE ACCOUNT")

        if success:
            self.statusLbl.setStyleSheet(_OK_SS)
            self.statusLbl.setText("✓ Account created! You can now sign in.")
            self.registerBtn.setEnabled(False)
        else:
            self._err(msg)

    def _err(self, text: str):
        self.statusLbl.setStyleSheet(_ERR_SS)
        self.statusLbl.setText(text)