# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

base_dir   = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")

# ══════════════════════════════════════════════════════════════════════════════
#  Style constants
# ══════════════════════════════════════════════════════════════════════════════
_PANEL_LEFT_SS = "QWidget#panelLeft { background-color: #1B4332; }"
_PANEL_RIGHT_SS = "QWidget#panelRight { background-color: #F8FBF9; }"
_LOGO_LABEL_SS = "background: transparent; border: none;"

_BRAND_TITLE_SS = """
QLabel { background: transparent; border: none; color: #C6F6D5;
    font: bold 22pt 'Georgia'; letter-spacing: 4px; }"""

_BRAND_SUB_SS = """
QLabel { background: transparent; border: none;
    color: rgba(198,246,213,0.55); font: 9pt 'Segoe UI'; letter-spacing: 3px; }"""

_BRAND_RULE_SS = """
QFrame { background-color: rgba(198,246,213,0.30); border: none; max-height: 1px; }"""

_BRAND_TAGLINE_SS = """
QLabel { background: transparent; border: none;
    color: rgba(198,246,213,0.45); font: italic 9pt 'Georgia'; }"""

_FORM_HEADING_SS = """
QLabel { background: transparent; border: none;
    color: #1B4332; font: bold 20pt 'Georgia'; }"""

_FORM_SUB_SS = """
QLabel { background: transparent; border: none;
    color: #6B8F78; font: 9pt 'Segoe UI'; letter-spacing: 1px; }"""

_FIELD_LABEL_SS = """
QLabel { background: transparent; border: none; color: #2D6A4F;
    font: bold 8pt 'Segoe UI'; letter-spacing: 2px; }"""

_INPUT_SS = """
QLineEdit {
    background-color: #FFFFFF; color: #1B4332;
    border: 1.5px solid #D4E6DA; border-radius: 8px;
    padding: 10px 14px; font: 11pt 'Segoe UI';
    selection-background-color: #C6F6D5;
}
QLineEdit:hover  { border: 1.5px solid #74C69D; background-color: #F4FBF7; }
QLineEdit:focus  { border: 2px solid #2D6A4F; background-color: #FFFFFF; }
"""

_LOGIN_BTN_SS = """
QPushButton {
    background-color: #2D6A4F; color: #FFFFFF; border: none;
    border-radius: 8px; font: bold 10pt 'Segoe UI';
    letter-spacing: 3px; padding: 12px;
}
QPushButton:hover    { background-color: #1B4332; }
QPushButton:pressed  { background-color: #081C15; }
QPushButton:disabled { background-color: #B7D5C4; color: rgba(255,255,255,0.60); }
"""

_FOOTER_SS = """
QLabel { background: transparent; border: none;
    color: #A0B8AB; font: 8pt 'Segoe UI'; }"""

_VERSION_SS = """
QLabel { background: transparent; border: none;
    color: rgba(198,246,213,0.35); font: 8pt 'Segoe UI'; letter-spacing: 1px; }"""


# ══════════════════════════════════════════════════════════════════════════════
#  UI class
# ══════════════════════════════════════════════════════════════════════════════
class Ui_Login(object):

    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.setFixedSize(820, 500)          # ← taller to fit new buttons
        Login.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Login.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        Login.setStyleSheet("QMainWindow { background: transparent; }")

        self.centralwidget = QtWidgets.QWidget(Login)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-color: #F8FBF9;
                border-radius: 18px;
            }
        """)
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50); shadow.setOffset(0, 8)
        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.centralwidget.setGraphicsEffect(shadow)
        Login.setCentralWidget(self.centralwidget)

        h_split = QtWidgets.QHBoxLayout(self.centralwidget)
        h_split.setContentsMargins(0, 0, 0, 0)
        h_split.setSpacing(0)

        # ══════════════════════════════════════════════════════════════════════
        #  LEFT PANEL
        # ══════════════════════════════════════════════════════════════════════
        self.panelLeft = QtWidgets.QWidget()
        self.panelLeft.setObjectName("panelLeft")
        self.panelLeft.setFixedWidth(300)
        self.panelLeft.setStyleSheet(_PANEL_LEFT_SS)

        left_layout = QtWidgets.QVBoxLayout(self.panelLeft)
        left_layout.setContentsMargins(36, 48, 36, 36)
        left_layout.setSpacing(0)
        left_layout.setAlignment(QtCore.Qt.AlignTop)

        self.Logo = QtWidgets.QLabel()
        self.Logo.setFixedSize(90, 90)
        self.Logo.setPixmap(
            QtGui.QPixmap(f"{image_path}/Logo.png").scaled(
                90, 90, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.Logo.setScaledContents(True)
        self.Logo.setStyleSheet(_LOGO_LABEL_SS)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        left_layout.addWidget(self.Logo, 0, QtCore.Qt.AlignHCenter)
        left_layout.addSpacing(22)

        rule_top = QtWidgets.QFrame()
        rule_top.setFrameShape(QtWidgets.QFrame.HLine)
        rule_top.setStyleSheet(_BRAND_RULE_SS)
        left_layout.addWidget(rule_top)
        left_layout.addSpacing(14)

        self.brandTitle = QtWidgets.QLabel("RAIONN")
        self.brandTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.brandTitle.setStyleSheet(_BRAND_TITLE_SS)
        left_layout.addWidget(self.brandTitle)
        left_layout.addSpacing(4)

        self.brandSub = QtWidgets.QLabel("A D M I N   S Y S T E M")
        self.brandSub.setAlignment(QtCore.Qt.AlignCenter)
        self.brandSub.setStyleSheet(_BRAND_SUB_SS)
        left_layout.addWidget(self.brandSub)
        left_layout.addSpacing(14)

        rule_bot = QtWidgets.QFrame()
        rule_bot.setFrameShape(QtWidgets.QFrame.HLine)
        rule_bot.setStyleSheet(_BRAND_RULE_SS)
        left_layout.addWidget(rule_bot)
        left_layout.addSpacing(24)

        self.brandTagline = QtWidgets.QLabel("Secure  ·  Reliable  ·  Efficient")
        self.brandTagline.setAlignment(QtCore.Qt.AlignCenter)
        self.brandTagline.setStyleSheet(_BRAND_TAGLINE_SS)
        self.brandTagline.setWordWrap(True)
        left_layout.addWidget(self.brandTagline)
        left_layout.addStretch()

        self.versionLabel = QtWidgets.QLabel("v 1.0.0")
        self.versionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.versionLabel.setStyleSheet(_VERSION_SS)
        left_layout.addWidget(self.versionLabel)

        h_split.addWidget(self.panelLeft)

        # ══════════════════════════════════════════════════════════════════════
        #  RIGHT PANEL
        # ══════════════════════════════════════════════════════════════════════
        self.panelRight = QtWidgets.QWidget()
        self.panelRight.setObjectName("panelRight")
        self.panelRight.setStyleSheet(_PANEL_RIGHT_SS)

        right_layout = QtWidgets.QVBoxLayout(self.panelRight)
        right_layout.setContentsMargins(52, 0, 52, 0)
        right_layout.setSpacing(0)

        # ── Close button ──────────────────────────────────────────────────────
        top_bar = QtWidgets.QHBoxLayout()
        top_bar.setContentsMargins(0, 16, 0, 0)
        top_bar.addStretch()
        self.closeBtn = QtWidgets.QPushButton("✕")
        self.closeBtn.setFixedSize(28, 28)
        self.closeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeBtn.setStyleSheet("""
            QPushButton { background: transparent; border: none; color: #A0B8AB;
                font: bold 11pt 'Segoe UI'; border-radius: 14px; }
            QPushButton:hover { background-color: #E8F5EE; color: #1B4332; }
        """)
        self.closeBtn.clicked.connect(Login.close)
        top_bar.addWidget(self.closeBtn)
        top_widget = QtWidgets.QWidget()
        top_widget.setStyleSheet("background: transparent;")
        top_widget.setLayout(top_bar)
        right_layout.addWidget(top_widget)

        right_layout.addSpacing(12)       # ← reduced from addStretch

        # ── Heading ───────────────────────────────────────────────────────────
        self.formHeading = QtWidgets.QLabel("Welcome back")
        self.formHeading.setStyleSheet(_FORM_HEADING_SS)
        right_layout.addWidget(self.formHeading)
        right_layout.addSpacing(3)

        self.formSub = QtWidgets.QLabel("SIGN IN TO CONTINUE")
        self.formSub.setStyleSheet(_FORM_SUB_SS)
        right_layout.addWidget(self.formSub)
        right_layout.addSpacing(20)       # ← reduced from 36

        # ── Username ──────────────────────────────────────────────────────────
        self.usernameLabel = QtWidgets.QLabel("USERNAME")
        self.usernameLabel.setStyleSheet(_FIELD_LABEL_SS)
        right_layout.addWidget(self.usernameLabel)
        right_layout.addSpacing(5)

        self.usernameEdit = QtWidgets.QLineEdit()
        self.usernameEdit.setFixedHeight(44)
        self.usernameEdit.setPlaceholderText("Enter your username")
        self.usernameEdit.setObjectName("usernameEdit")
        self.usernameEdit.setStyleSheet(_INPUT_SS)
        right_layout.addWidget(self.usernameEdit)
        right_layout.addSpacing(14)       # ← reduced from 20

        # ── Password ──────────────────────────────────────────────────────────
        self.passwordLabel = QtWidgets.QLabel("PASSWORD")
        self.passwordLabel.setStyleSheet(_FIELD_LABEL_SS)
        right_layout.addWidget(self.passwordLabel)
        right_layout.addSpacing(5)

        pwd_wrapper = QtWidgets.QWidget()
        pwd_wrapper.setFixedHeight(44)
        pwd_wrapper.setStyleSheet("background: transparent; border: none;")
        pwd_stack = QtWidgets.QStackedLayout(pwd_wrapper)
        pwd_stack.setStackingMode(QtWidgets.QStackedLayout.StackAll)

        self.passwordEdit = QtWidgets.QLineEdit()
        self.passwordEdit.setFixedHeight(44)
        self.passwordEdit.setPlaceholderText("Enter your password")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.passwordEdit.setStyleSheet(_INPUT_SS)
        self.passwordEdit.setTextMargins(0, 0, 44, 0)

        eye_overlay = QtWidgets.QWidget()
        eye_overlay.setStyleSheet("background: transparent; border: none;")
        eye_h = QtWidgets.QHBoxLayout(eye_overlay)
        eye_h.setContentsMargins(0, 0, 6, 0)
        eye_h.addStretch()
        self.eyeBtn = QtWidgets.QPushButton("👁")
        self.eyeBtn.setFixedSize(34, 34)
        self.eyeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.eyeBtn.setCheckable(True)
        self.eyeBtn.setStyleSheet("""
            QPushButton { background: transparent; border: none;
                color: #A0B8AB; font: 12pt 'Segoe UI'; }
            QPushButton:hover { color: #2D6A4F; }
        """)
        self.eyeBtn.toggled.connect(self._toggle_password)
        eye_h.addWidget(self.eyeBtn, 0, QtCore.Qt.AlignVCenter)
        pwd_stack.addWidget(self.passwordEdit)
        pwd_stack.addWidget(eye_overlay)
        right_layout.addWidget(pwd_wrapper)
        right_layout.addSpacing(16)       # ← reduced from 32

        # ── Divider ───────────────────────────────────────────────────────────
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setStyleSheet("background-color: #E2EDE7; border: none; max-height: 1px;")
        right_layout.addWidget(divider)
        right_layout.addSpacing(16)       # ← reduced from 28

        # ── Login button ──────────────────────────────────────────────────────
        self.loginbutton = QtWidgets.QPushButton("SIGN IN")
        self.loginbutton.setFixedHeight(46)
        self.loginbutton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loginbutton.setObjectName("loginbutton")
        self.loginbutton.setStyleSheet(_LOGIN_BTN_SS)
        right_layout.addWidget(self.loginbutton)
        right_layout.addSpacing(8)

        # ── Forgot password link ──────────────────────────────────────────────
        forgot_row = QtWidgets.QHBoxLayout()
        forgot_row.addStretch()
        self.forgotBtn = QtWidgets.QPushButton("Forgot password?")
        self.forgotBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.forgotBtn.setStyleSheet("""
            QPushButton { background: transparent; border: none;
                color: #6B8F78; font: 9pt 'Segoe UI'; text-decoration: underline; }
            QPushButton:hover { color: #2D6A4F; }
        """)
        forgot_row.addWidget(self.forgotBtn)
        forgot_row.addStretch()
        right_layout.addLayout(forgot_row)
        right_layout.addSpacing(14)

        # ── OR divider ────────────────────────────────────────────────────────
        or_row = QtWidgets.QHBoxLayout()
        or_row.setSpacing(10)
        _line1 = QtWidgets.QFrame()
        _line1.setFrameShape(QtWidgets.QFrame.HLine)
        _line1.setStyleSheet("background: #E2EDE7; max-height: 1px; border: none;")
        _or_lbl = QtWidgets.QLabel("OR")
        _or_lbl.setStyleSheet(
            "color: #A0B8AB; font: 8pt 'Segoe UI'; background: transparent; border: none;")
        _line2 = QtWidgets.QFrame()
        _line2.setFrameShape(QtWidgets.QFrame.HLine)
        _line2.setStyleSheet("background: #E2EDE7; max-height: 1px; border: none;")
        or_row.addWidget(_line1, 1)
        or_row.addWidget(_or_lbl)
        or_row.addWidget(_line2, 1)
        right_layout.addLayout(or_row)
        right_layout.addSpacing(14)

        # ── Register button ───────────────────────────────────────────────────
        self.registerBtn = QtWidgets.QPushButton("Create a new account")
        self.registerBtn.setFixedHeight(44)
        self.registerBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.registerBtn.setObjectName("registerBtn")
        self.registerBtn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #2D6A4F;
                border: 1.5px solid #2D6A4F; border-radius: 8px;
                font: 500 10pt 'Segoe UI'; letter-spacing: 1px;
            }
            QPushButton:hover   { background: #EBF7F0; border-color: #1B4332; color: #1B4332; }
            QPushButton:pressed { background: #D4EDE2; }
        """)
        right_layout.addWidget(self.registerBtn)

        right_layout.addStretch(1)

        # ── Footer ────────────────────────────────────────────────────────────
        self.footerLabel = QtWidgets.QLabel(
            "© 2025 Raionn Admin System. All rights reserved.")
        self.footerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.footerLabel.setStyleSheet(_FOOTER_SS)
        right_layout.addWidget(self.footerLabel)
        right_layout.addSpacing(14)

        h_split.addWidget(self.panelRight)

        # ── Window drag ───────────────────────────────────────────────────────
        self._drag_start = None
        Login.mousePressEvent   = self._mouse_press
        Login.mouseMoveEvent    = self._mouse_move
        Login.mouseReleaseEvent = self._mouse_release

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _toggle_password(self, checked):
        if checked:
            self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.eyeBtn.setText("🙈")
        else:
            self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.eyeBtn.setText("👁")

    def _mouse_press(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start = event.globalPos()

    def _mouse_move(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self._drag_start is not None:
            delta = event.globalPos() - self._drag_start
            win = self.centralwidget.parent()
            win.move(win.pos() + delta)
            self._drag_start = event.globalPos()

    def _mouse_release(self, event):
        self._drag_start = None

    def retranslateUi(self, Login):
        Login.setWindowTitle(
            QtCore.QCoreApplication.translate("Login", "Raionn Admin — Login"))


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Login = QtWidgets.QMainWindow()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())