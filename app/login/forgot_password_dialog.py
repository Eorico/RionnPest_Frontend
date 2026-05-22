# login/forgot_password_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QStackedWidget,
    QGraphicsDropShadowEffect, QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QColor, QCursor, QFont

_G400   = "#2D6A4F"
_G600   = "#1B4332"
_G100   = "#C6F6D5"
_BG     = "#F8FBF9"
_BORDER = "#D4E6DA"
_MUTED  = "#6B8F78"

_INPUT_SS = """
QLineEdit {
    background: #FFFFFF; color: #1B4332;
    border: 1.5px solid #D4E6DA; border-radius: 8px;
    padding: 10px 14px; font: 10pt 'Segoe UI';
}
QLineEdit:focus { border: 2px solid #2D6A4F; background: #FAFFFE; }
QLineEdit:hover { border-color: #74C69D; }
"""
_OTP_SS = """
QLineEdit {
    background: #F0FAF4; color: #1B4332;
    border: 2px solid #74C69D; border-radius: 10px;
    font: bold 22pt 'Segoe UI'; letter-spacing: 12px;
    padding: 14px; qproperty-alignment: AlignCenter;
}
QLineEdit:focus { border-color: #2D6A4F; background: #FFFFFF; }
"""
_BTN_PRIMARY_SS = f"""
QPushButton {{
    background: {_G400}; color: #fff; border: none;
    border-radius: 8px; font: 600 10pt 'Segoe UI';
    letter-spacing: 1px; padding: 12px;
}}
QPushButton:hover    {{ background: {_G600}; }}
QPushButton:pressed  {{ background: #081C15; }}
QPushButton:disabled {{ background: #B7D5C4; color: rgba(255,255,255,0.6); }}
"""
_BTN_LINK_SS = f"""
QPushButton {{
    background: transparent; border: none;
    color: {_MUTED}; font: 9pt 'Segoe UI';
}}
QPushButton:hover {{ color: {_G400}; text-decoration: underline; }}
"""
_LBL_CAP_SS = f"""
QLabel {{ background: transparent; border: none; color: {_G400};
    font: 700 8pt 'Segoe UI'; letter-spacing: 1.5px; }}
"""
_ERR_SS = """QLabel { color: #DC2626; font: 9pt 'Segoe UI';
    background: #FEF2F2; border: 1px solid #FECACA;
    border-radius: 6px; padding: 8px 12px; }"""
_OK_SS  = f"""QLabel {{ color: {_G400}; font: 9pt 'Segoe UI';
    background: #F0FAF4; border: 1px solid {_G100};
    border-radius: 6px; padding: 8px 12px; }}"""
_HIDDEN_SS = "QLabel { background: transparent; border: none; }"


class ForgotPasswordDialog(QDialog):
    def __init__(self, api_service, parent=None):
        super().__init__(parent)
        self.api             = api_service
        self._username       = ""
        self._drag           = None
        self._resend_seconds = 0
        self._resend_timer   = QTimer(self)
        self._resend_timer.timeout.connect(self._tick_resend)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(460)
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)

        self._card = QFrame()
        self._card.setStyleSheet(f"""
            QFrame {{
                background: {_BG};
                border-radius: 18px;
                border: 1px solid {_BORDER};
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(48)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 65))
        self._card.setGraphicsEffect(shadow)
        outer.addWidget(self._card)

        root = QVBoxLayout(self._card)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Colored top band ──────────────────────────────────────────────────
        band = QFrame()
        band.setFixedHeight(6)
        band.setStyleSheet(f"background: {_G400}; border-radius: 18px 18px 0 0;")
        root.addWidget(band)

        # ── Content area ──────────────────────────────────────────────────────
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(40, 28, 40, 32)
        content_lay.setSpacing(0)

        # Close button row
        close_row = QHBoxLayout()
        close_row.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton { background: transparent; border: none;
                color: #A0B8AB; font: bold 11pt 'Segoe UI'; border-radius: 14px; }
            QPushButton:hover { background: #E8F5EE; color: #1B4332; }
        """)
        close_btn.clicked.connect(self.reject)
        close_row.addWidget(close_btn)
        content_lay.addLayout(close_row)
        content_lay.addSpacing(4)

        # Icon
        icon_lbl = QLabel("🔐")
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(
            "font: 36pt 'Segoe UI'; background: transparent; border: none;")
        content_lay.addWidget(icon_lbl)
        content_lay.addSpacing(10)

        # Title + subtitle (updatable)
        self._title = QLabel("Forgot Password")
        self._title.setAlignment(Qt.AlignCenter)
        self._title.setStyleSheet(
            f"color: {_G600}; font: bold 20pt 'Georgia';"
            f" background: transparent; border: none;")
        content_lay.addWidget(self._title)
        content_lay.addSpacing(6)

        self._subtitle = QLabel("Enter your username to receive a reset code.")
        self._subtitle.setAlignment(Qt.AlignCenter)
        self._subtitle.setWordWrap(True)
        self._subtitle.setStyleSheet(
            f"color: {_MUTED}; font: 9pt 'Segoe UI';"
            f" background: transparent; border: none;")
        content_lay.addWidget(self._subtitle)
        content_lay.addSpacing(24)

        # Stacked pages
        self._stack = QStackedWidget()
        self._stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._stack.addWidget(self._build_step1())
        self._stack.addWidget(self._build_step2())
        content_lay.addWidget(self._stack)

        root.addWidget(content)

        # Drag
        self._card.mousePressEvent   = self._drag_press
        self._card.mouseMoveEvent    = self._drag_move
        self._card.mouseReleaseEvent = self._drag_release

    def _build_step1(self) -> QWidget:
        w   = QWidget(); w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        lbl = QLabel("USERNAME")
        lbl.setStyleSheet(_LBL_CAP_SS)
        lay.addWidget(lbl)
        lay.addSpacing(6)

        self.usernameEdit = QLineEdit()
        self.usernameEdit.setFixedHeight(44)
        self.usernameEdit.setPlaceholderText("Enter your username")
        self.usernameEdit.setStyleSheet(_INPUT_SS)
        self.usernameEdit.returnPressed.connect(self._send_code)
        lay.addWidget(self.usernameEdit)
        lay.addSpacing(14)

        # Status (hidden by default)
        self._step1Status = QLabel("")
        self._step1Status.setWordWrap(True)
        self._step1Status.setStyleSheet(_HIDDEN_SS)
        self._step1Status.setFixedHeight(0)
        lay.addWidget(self._step1Status)
        lay.addSpacing(6)

        self._sendBtn = QPushButton("SEND RESET CODE")
        self._sendBtn.setFixedHeight(46)
        self._sendBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self._sendBtn.setStyleSheet(_BTN_PRIMARY_SS)
        self._sendBtn.clicked.connect(self._send_code)
        lay.addWidget(self._sendBtn)
        lay.addSpacing(16)

        # Back link
        back_row = QHBoxLayout()
        back_row.addStretch()
        back_btn = QPushButton("← Back to sign in")
        back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        back_btn.setStyleSheet(_BTN_LINK_SS)
        back_btn.clicked.connect(self.reject)
        back_row.addWidget(back_btn)
        back_row.addStretch()
        lay.addLayout(back_row)
        return w

    def _build_step2(self) -> QWidget:
        w   = QWidget(); w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Sent confirmation chip
        self._codeSentLbl = QLabel("")
        self._codeSentLbl.setWordWrap(True)
        self._codeSentLbl.setAlignment(Qt.AlignCenter)
        self._codeSentLbl.setStyleSheet(_HIDDEN_SS)
        lay.addWidget(self._codeSentLbl)
        lay.addSpacing(14)

        # OTP box
        otp_lbl = QLabel("VERIFICATION CODE")
        otp_lbl.setStyleSheet(_LBL_CAP_SS)
        lay.addWidget(otp_lbl)
        lay.addSpacing(6)

        self.otpEdit = QLineEdit()
        self.otpEdit.setFixedHeight(60)
        self.otpEdit.setMaxLength(6)
        self.otpEdit.setAlignment(Qt.AlignCenter)
        self.otpEdit.setPlaceholderText("• • • • • •")
        self.otpEdit.setStyleSheet(_OTP_SS)
        lay.addWidget(self.otpEdit)
        lay.addSpacing(18)

        # Divider
        div = QFrame(); div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("background: #E2EDE7; max-height: 1px; border: none;")
        lay.addWidget(div)
        lay.addSpacing(18)

        # New password
        pw_lbl = QLabel("NEW PASSWORD")
        pw_lbl.setStyleSheet(_LBL_CAP_SS)
        lay.addWidget(pw_lbl)
        lay.addSpacing(6)
        self.newPwEdit = QLineEdit()
        self.newPwEdit.setFixedHeight(44)
        self.newPwEdit.setEchoMode(QLineEdit.Password)
        self.newPwEdit.setPlaceholderText("At least 8 characters")
        self.newPwEdit.setStyleSheet(_INPUT_SS)
        lay.addWidget(self.newPwEdit)
        lay.addSpacing(10)

        confirm_lbl = QLabel("CONFIRM PASSWORD")
        confirm_lbl.setStyleSheet(_LBL_CAP_SS)
        lay.addWidget(confirm_lbl)
        lay.addSpacing(6)
        self.confirmPwEdit = QLineEdit()
        self.confirmPwEdit.setFixedHeight(44)
        self.confirmPwEdit.setEchoMode(QLineEdit.Password)
        self.confirmPwEdit.setPlaceholderText("Repeat new password")
        self.confirmPwEdit.setStyleSheet(_INPUT_SS)
        lay.addWidget(self.confirmPwEdit)
        lay.addSpacing(14)

        # Status
        self._step2Status = QLabel("")
        self._step2Status.setWordWrap(True)
        self._step2Status.setStyleSheet(_HIDDEN_SS)
        lay.addWidget(self._step2Status)
        lay.addSpacing(6)

        self._resetBtn = QPushButton("RESET PASSWORD")
        self._resetBtn.setFixedHeight(46)
        self._resetBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self._resetBtn.setStyleSheet(_BTN_PRIMARY_SS)
        self._resetBtn.clicked.connect(self._reset_password)
        lay.addWidget(self._resetBtn)
        lay.addSpacing(16)

        # Resend + back row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        bottom_row.addStretch()
        self._resendBtn = QPushButton("Resend code")
        self._resendBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self._resendBtn.setStyleSheet(_BTN_LINK_SS)
        self._resendBtn.clicked.connect(self._resend_code)
        bottom_row.addWidget(self._resendBtn)

        sep = QLabel("·")
        sep.setStyleSheet(f"color: {_MUTED}; background: transparent; border: none;")
        bottom_row.addWidget(sep)

        back_btn = QPushButton("← Back")
        back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        back_btn.setStyleSheet(_BTN_LINK_SS)
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        bottom_row.addWidget(back_btn)
        bottom_row.addStretch()
        lay.addLayout(bottom_row)
        return w

    # ── Drag ─────────────────────────────────────────────────────────────────
    def _drag_press(self, e):
        if e.button() == Qt.LeftButton:
            self._drag = e.globalPos()

    def _drag_move(self, e):
        if e.buttons() == Qt.LeftButton and self._drag is not None:
            self.move(self.pos() + e.globalPos() - self._drag)
            self._drag = e.globalPos()

    def _drag_release(self, e):
        self._drag = None

    # ── Step 1 ────────────────────────────────────────────────────────────────
    def _send_code(self):
        username = self.usernameEdit.text().strip()
        if not username:
            self._show_status(self._step1Status, "Please enter your username.", error=True)
            return

        self._sendBtn.setEnabled(False)
        self._sendBtn.setText("Sending…")
        self._step1Status.setStyleSheet(_HIDDEN_SS)
        self._step1Status.setFixedHeight(0)

        success, msg = self.api.forgot_password_service(username)

        self._sendBtn.setEnabled(True)
        self._sendBtn.setText("SEND RESET CODE")

        if success:
            self._username = username
            self._title.setText("Check Your Gmail")
            self._subtitle.setText(
                f"A 6-digit code was sent to:\n{msg}\n"
                f"Enter it below to reset your password."
            )
            self._show_status(self._codeSentLbl, f"✓ Code sent to {msg}", error=False)
            self.otpEdit.clear()
            self.newPwEdit.clear()
            self.confirmPwEdit.clear()
            self._step2Status.setStyleSheet(_HIDDEN_SS)
            self._stack.setCurrentIndex(1)
            self.adjustSize()
            self._start_resend_cooldown(60)
        else:
            self._show_status(self._step1Status, msg, error=True)

    # ── Step 2 ────────────────────────────────────────────────────────────────
    def _reset_password(self):
        otp        = self.otpEdit.text().strip()
        new_pw     = self.newPwEdit.text()
        confirm_pw = self.confirmPwEdit.text()

        if len(otp) != 6 or not otp.isdigit():
            self._show_status(self._step2Status,
                              "Enter the 6-digit code from your email.", error=True)
            return
        if len(new_pw) < 8:
            self._show_status(self._step2Status,
                              "Password must be at least 8 characters.", error=True)
            return
        if new_pw != confirm_pw:
            self._show_status(self._step2Status,
                              "Passwords do not match.", error=True)
            return

        self._resetBtn.setEnabled(False)
        self._resetBtn.setText("Resetting…")

        success, msg = self.api.reset_password_service(self._username, otp, new_pw)

        self._resetBtn.setEnabled(True)
        self._resetBtn.setText("RESET PASSWORD")

        if success:
            self._show_status(self._step2Status,
                              "✓ Password reset! You can now sign in.", error=False)
            self._resetBtn.setEnabled(False)
            self._resendBtn.setEnabled(False)
            self._resend_timer.stop()
        else:
            self._show_status(self._step2Status, msg, error=True)

    def _resend_code(self):
        success, msg = self.api.forgot_password_service(self._username)
        if success:
            self._show_status(self._codeSentLbl, f"✓ New code sent to {msg}", error=False)
            self._start_resend_cooldown(60)
        else:
            self._show_status(self._step2Status, msg, error=True)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _show_status(self, lbl: QLabel, text: str, error: bool):
        lbl.setStyleSheet(_ERR_SS if error else _OK_SS)
        lbl.setText(text)
        lbl.setFixedHeight(lbl.sizeHint().height() + 8)

    def _start_resend_cooldown(self, seconds: int):
        self._resend_seconds = seconds
        self._resendBtn.setEnabled(False)
        self._tick_resend()
        self._resend_timer.start(1000)

    def _tick_resend(self):
        if self._resend_seconds <= 0:
            self._resend_timer.stop()
            self._resendBtn.setEnabled(True)
            self._resendBtn.setText("Resend code")
        else:
            self._resendBtn.setText(f"Resend ({self._resend_seconds}s)")
            self._resend_seconds -= 1