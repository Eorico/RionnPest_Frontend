# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

base_dir   = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")


# ══════════════════════════════════════════════════════════════════════════════
#  Style constants
# ══════════════════════════════════════════════════════════════════════════════
_PROGRESS_SS = """
QProgressBar {
    background-color: rgba(255, 255, 255, 0.12);
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
}
QProgressBar::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0   #52B788,
        stop:0.5 #74C69D,
        stop:1   #C6F6D5
    );
    border-radius: 4px;
}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  Animated dots helper
# ══════════════════════════════════════════════════════════════════════════════
class _DotTimer(QtCore.QObject):
    """Cycles the loading label through  'Loading ●○○' → '●●○' → '●●●' → …"""
    def __init__(self, label: QtWidgets.QLabel, parent=None):
        super().__init__(parent)
        self._label = label
        self._step  = 0
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(420)

    def _tick(self):
        dots = ["●○○", "●●○", "●●●", "○○○"]
        self._label.setText(f"Loading  {dots[self._step % 4]}")
        self._step += 1

    def stop(self):
        self._timer.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  UI class
# ══════════════════════════════════════════════════════════════════════════════
class Ui_Intro(object):

    def setupUi(self, Intro):
        Intro.setObjectName("Intro")
        Intro.setFixedSize(820, 480)
        Intro.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Intro.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        Intro.setStyleSheet("QMainWindow { background: transparent; }")

        # ── Central widget (the card) ─────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(Intro)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-color: #0D1F17;
            }
        """)

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setOffset(0, 10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 120))
        self.centralwidget.setGraphicsEffect(shadow)

        Intro.setCentralWidget(self.centralwidget)

        # ── Root layout ───────────────────────────────────────────────────────
        root = QtWidgets.QVBoxLayout(self.centralwidget)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ══════════════════════════════════════════════════════════════════════
        #  TOP: background image with dark overlay
        # ══════════════════════════════════════════════════════════════════════
        self.bgContainer = QtWidgets.QWidget()
        self.bgContainer.setObjectName("bgContainer")
        self.bgContainer.setMinimumHeight(340)
        self.bgContainer.setStyleSheet("""
            QWidget#bgContainer {
                background-color: #1B4332;
                border-top-left-radius: 18px;
                border-top-right-radius: 18px;
            }
        """)

        bg_stack = QtWidgets.QStackedLayout(self.bgContainer)
        bg_stack.setStackingMode(QtWidgets.QStackedLayout.StackAll)

        # Background image layer
        self.bgImage = QtWidgets.QLabel()
        self.bgImage.setScaledContents(True)
        self.bgImage.setStyleSheet("""
            QLabel {
                border-top-left-radius: 18px;
                border-top-right-radius: 18px;
            }
        """)
        px = QtGui.QPixmap(
            f"{image_path}/ac5ef8e8-980b-4953-9c2c-731a2af90d63.jpg")
        if not px.isNull():
            self.bgImage.setPixmap(px)

        # Dark gradient overlay layer
        self.overlay = QtWidgets.QWidget()
        self.overlay.setObjectName("overlay")
        self.overlay.setStyleSheet("""
            QWidget#overlay {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0   rgba(13,  31, 23, 0.35),
                    stop:0.5 rgba(13,  31, 23, 0.55),
                    stop:1   rgba(13,  31, 23, 0.92)
                );
                border-top-left-radius: 18px;
                border-top-right-radius: 18px;
            }
        """)

        # Content layer (logo + title centred over the image)
        content_layer = QtWidgets.QWidget()
        content_layer.setStyleSheet("background: transparent;")
        content_v = QtWidgets.QVBoxLayout(content_layer)
        content_v.setContentsMargins(40, 40, 40, 30)
        content_v.setSpacing(0)
        content_v.setAlignment(QtCore.Qt.AlignCenter)

        # Logo
        self.Logo = QtWidgets.QLabel()
        self.Logo.setFixedSize(100, 100)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setStyleSheet("background: transparent; border: none;")
        logo_px = QtGui.QPixmap(f"{image_path}/Logo.png").scaled(
            100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        if not logo_px.isNull():
            self.Logo.setPixmap(logo_px)
        content_v.addWidget(self.Logo, 0, QtCore.Qt.AlignHCenter)

        content_v.addSpacing(18)

        # Brand name
        self.brandName = QtWidgets.QLabel("RAIONN")
        self.brandName.setAlignment(QtCore.Qt.AlignCenter)
        self.brandName.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                color: #FFFFFF;
                font: bold 38pt 'Georgia';
                letter-spacing: 10px;
            }
        """)
        content_v.addWidget(self.brandName)

        content_v.addSpacing(6)

        # Sub-title
        self.brandSub = QtWidgets.QLabel("A D M I N   S Y S T E M")
        self.brandSub.setAlignment(QtCore.Qt.AlignCenter)
        self.brandSub.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                color: rgba(198, 246, 213, 0.70);
                font: 10pt 'Segoe UI';
                letter-spacing: 5px;
            }
        """)
        content_v.addWidget(self.brandSub)

        content_v.addSpacing(20)

        # Thin decorative rule
        rule = QtWidgets.QFrame()
        rule.setFrameShape(QtWidgets.QFrame.HLine)
        rule.setFixedWidth(180)
        rule.setStyleSheet("""
            QFrame {
                background-color: rgba(198, 246, 213, 0.35);
                border: none;
                max-height: 1px;
            }
        """)
        content_v.addWidget(rule, 0, QtCore.Qt.AlignHCenter)

        content_v.addSpacing(14)

        # Tagline
        self.tagline = QtWidgets.QLabel("Secure  ·  Reliable  ·  Efficient")
        self.tagline.setAlignment(QtCore.Qt.AlignCenter)
        self.tagline.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                color: rgba(198, 246, 213, 0.45);
                font: italic 10pt 'Georgia';
                letter-spacing: 1px;
            }
        """)
        content_v.addWidget(self.tagline)

        # Stack: image → overlay → content
        bg_stack.addWidget(self.bgImage)
        bg_stack.addWidget(self.overlay)
        bg_stack.addWidget(content_layer)

        root.addWidget(self.bgContainer)

        # ══════════════════════════════════════════════════════════════════════
        #  BOTTOM: progress strip
        # ══════════════════════════════════════════════════════════════════════
        self.bottomBar = QtWidgets.QWidget()
        self.bottomBar.setObjectName("bottomBar")
        self.bottomBar.setFixedHeight(140)
        self.bottomBar.setStyleSheet("""
            QWidget#bottomBar {
                background-color: #0D1F17;
                border-bottom-left-radius: 18px;
                border-bottom-right-radius: 18px;
            }
        """)

        bottom_v = QtWidgets.QVBoxLayout(self.bottomBar)
        bottom_v.setContentsMargins(52, 24, 52, 28)
        bottom_v.setSpacing(12)

        # Status / indicator label
        self.indicator = QtWidgets.QLabel("Loading  ●○○")
        self.indicator.setAlignment(QtCore.Qt.AlignCenter)
        self.indicator.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                color: rgba(198, 246, 213, 0.65);
                font: 10pt 'Segoe UI';
                letter-spacing: 2px;
            }
        """)
        bottom_v.addWidget(self.indicator)

        # Progress bar
        self.Progress_Loader = QtWidgets.QProgressBar()
        self.Progress_Loader.setObjectName("Progress_Loader")
        self.Progress_Loader.setFixedHeight(6)
        self.Progress_Loader.setTextVisible(False)
        self.Progress_Loader.setRange(0, 100)
        self.Progress_Loader.setValue(0)
        self.Progress_Loader.setStyleSheet(_PROGRESS_SS)
        bottom_v.addWidget(self.Progress_Loader)

        # Version + copyright row
        meta_row = QtWidgets.QHBoxLayout()
        meta_row.setContentsMargins(0, 4, 0, 0)

        self.versionLabel = QtWidgets.QLabel("v 1.0.0")
        self.versionLabel.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                color: rgba(198, 246, 213, 0.25);
                font: 8pt 'Segoe UI';
            }
        """)
        meta_row.addWidget(self.versionLabel)
        meta_row.addStretch()

        self.copyrightLabel = QtWidgets.QLabel(
            "© 2025 Raionn Admin System")
        self.copyrightLabel.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                color: rgba(198, 246, 213, 0.25);
                font: 8pt 'Segoe UI';
            }
        """)
        meta_row.addWidget(self.copyrightLabel)
        bottom_v.addLayout(meta_row)

        root.addWidget(self.bottomBar)

        # ── Animated loading dots ─────────────────────────────────────────────
        self._dot_timer = _DotTimer(self.indicator, parent=self.centralwidget)

        self.retranslateUi(Intro)
        QtCore.QMetaObject.connectSlotsByName(Intro)

    def retranslateUi(self, Intro):
        Intro.setWindowTitle(
            QtCore.QCoreApplication.translate("Intro", "Raionn Admin"))


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    Intro = QtWidgets.QMainWindow()
    ui = Ui_Intro()
    ui.setupUi(Intro)
    Intro.show()
    sys.exit(app.exec_())