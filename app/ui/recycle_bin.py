# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QTimer, pyqtProperty, QEvent, QPoint
)
import os

base_dir   = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")

# ── Shared theme tokens ───────────────────────────────────────────────────────
_G100  = "#C6F6D5"
_G200  = "#74C69D"
_G400  = "#2D6A4F"
_G600  = "#1B4332"
_G800  = "#081C15"

_SURFACE    = "#FFFFFF"
_BG         = "#F4FAF7"
_TEXT       = _G600
_MUTED      = "#6B8F78"
_BORDER     = "#E0EDE6"
_HEADER_BG  = _G400

# ── Stylesheets ───────────────────────────────────────────────────────────────
_TABLE_SS = f"""
QTableWidget {{
    background: {_SURFACE};
    alternate-background-color: {_BG};
    gridline-color: {_BORDER};
    border: none;
    font: 10pt 'Segoe UI';
    color: {_TEXT};
    selection-background-color: {_G100};
    selection-color: {_TEXT};
}}
QTableWidget::item {{
    padding: 10px 14px;
    border: none;
    color: {_TEXT};
}}
QTableWidget::item:hover    {{ background: #E8F5EE; }}
QTableWidget::item:selected {{ background: {_G100}; color: {_TEXT}; }}
QHeaderView::section {{
    background: {_G400};
    color: #fff;
    border: none;
    border-right: 1px solid {_G600};
    padding: 10px 14px;
    font: 600 10pt 'Segoe UI';
    letter-spacing: 0.3px;
}}
QHeaderView::section:vertical {{
    background: {_BG};
    color: {_MUTED};
    border-right: 1px solid {_BORDER};
    font: 9pt 'Segoe UI';
    padding: 4px;
}}
QHeaderView {{ background: transparent; border: none; }}
QTableCornerButton::section {{ background: {_G400}; border: none; }}
QScrollBar:vertical {{
    background: {_BG}; width: 6px; border-radius: 3px; margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {_G200}; border-radius: 3px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover  {{ background: {_G400}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {_BG}; height: 6px; border-radius: 3px; margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: {_G200}; border-radius: 3px; min-width: 20px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""

_RESTORE_BTN_SS = f"""
QPushButton {{
    background: rgba(198,246,213,0.18);
    border: 1.5px solid rgba(198,246,213,0.45);
    border-radius: 10px;
}}
QPushButton:hover {{
    background: rgba(198,246,213,0.35);
    border-color: rgba(198,246,213,0.80);
}}
QPushButton:pressed {{
    background: rgba(198,246,213,0.10);
    border-color: rgba(198,246,213,0.30);
}}
"""

_DELETE_BTN_SS = """
QPushButton {
    background: rgba(220,38,38,0.18);
    border: 1.5px solid rgba(255,100,100,0.45);
    border-radius: 10px;
}
QPushButton:hover {
    background: rgba(220,38,38,0.38);
    border-color: rgba(255,100,100,0.85);
}
QPushButton:pressed {
    background: rgba(220,38,38,0.55);
    border-color: rgba(255,80,80,0.50);
}
"""

_CAPTION_IDLE_SS = """
QPushButton {
    background: transparent;
    color: rgba(255,255,255,0.75);
    border: none;
    border-radius: 0px;
    font: 10pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Segoe UI', sans-serif;
    min-width: 46px;
    min-height: 64px;
    max-height: 64px;
}
QPushButton:hover   { background: rgba(255,255,255,0.13); color: #fff; }
QPushButton:pressed { background: rgba(255,255,255,0.22); color: #fff; }
"""

_CAPTION_CLOSE_SS = """
QPushButton {
    background: transparent;
    color: rgba(255,255,255,0.85);
    border: none;
    border-radius: 0px;
    font: 10pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Segoe UI', sans-serif;
    min-width: 46px;
    min-height: 64px;
    max-height: 64px;
}
QPushButton:hover   { background: #C42B1C; color: #fff; }
QPushButton:pressed { background: #A31C12; color: #fff; }
"""

_LABEL_MUTED_SS = (
    f"color: {_MUTED}; font: 600 8pt 'Segoe UI'; "
    f"letter-spacing: 1.4px; background: transparent; border: none;"
)


# ══════════════════════════════════════════════════════════════════════════════
#  Custom tooltip — fully painted, bypasses Qt's broken tooltip on
#  frameless / WA_TranslucentBackground windows.
# ══════════════════════════════════════════════════════════════════════════════
class _CustomTooltip(QtWidgets.QWidget):
    """
    A standalone top-level widget that acts as a tooltip.
    We paint it ourselves so Qt's palette/fusion bugs don't apply.
    """
    _instance = None   # singleton

    def __init__(self):
        super().__init__(None, QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.setWindowFlags(
            QtCore.Qt.ToolTip
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.BypassGraphicsProxyWidget
        )
        self._text = ""
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show_tip(self, global_pos: QPoint, text: str, duration: int = 3000):
        if not text:
            self.hide()
            return
        self._text = text
        fm = QtGui.QFontMetrics(QtGui.QFont("Segoe UI", 9))
        text_rect = fm.boundingRect(text)
        pad_x, pad_y = 14, 8
        w = text_rect.width()  + pad_x * 2
        h = text_rect.height() + pad_y * 2
        self.setFixedSize(w, h)

        # Position: below and slightly right of the cursor
        screen = QtWidgets.QApplication.screenAt(global_pos)
        if screen:
            sr = screen.availableGeometry()
            x = min(global_pos.x() + 12, sr.right()  - w - 4)
            y = min(global_pos.y() + 20, sr.bottom() - h - 4)
        else:
            x = global_pos.x() + 12
            y = global_pos.y() + 20
        self.move(x, y)
        self.show()
        self.raise_()
        self._hide_timer.start(duration)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        # Background
        path = QtGui.QPainterPath()
        path.addRoundedRect(0.5, 0.5,
                            self.width() - 1, self.height() - 1,
                            6, 6)
        p.setBrush(QtGui.QColor("#FFFFFF"))
        p.setPen(QtGui.QPen(QtGui.QColor("#A8D5BA"), 1.0))
        p.drawPath(path)

        # Text
        p.setPen(QtGui.QColor("#1B4332"))
        p.setFont(QtGui.QFont("Segoe UI", 9))
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self._text)
        p.end()


class _TooltipFilter(QtCore.QObject):
    """
    Event filter installed on QApplication.
    Intercepts ToolTip events and shows our custom tooltip instead.
    """

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            widget = obj
            if isinstance(widget, QtWidgets.QWidget) and widget.toolTip():
                _CustomTooltip.instance().show_tip(
                    event.globalPos(), widget.toolTip())
            return True   # swallow the native tooltip
        if event.type() == QEvent.Leave:
            _CustomTooltip.instance().hide()
        return False


def install_custom_tooltips(app: QtWidgets.QApplication):
    """
    Call once after QApplication is created.
    Replaces ALL native tooltips with our white custom-painted ones.
    """
    f = _TooltipFilter(app)
    app.installEventFilter(f)
    # keep a reference so it doesn't get garbage-collected
    app._tooltip_filter = f


# ── Caption button helper ─────────────────────────────────────────────────────
def _caption_btn(symbol: str, close: bool = False, height: int = 64) -> QtWidgets.QPushButton:
    btn = QtWidgets.QPushButton(symbol)
    btn.setFixedSize(46, height)
    btn.setFlat(True)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    btn.setStyleSheet(_CAPTION_CLOSE_SS if close else _CAPTION_IDLE_SS)
    return btn


# ── Icon-only action button helper ───────────────────────────────────────────
def _icon_action_btn(
    icon_path: str,
    stylesheet: str,
    tooltip: str,
    icon_size: int = 26,
    btn_size: int = 44,
) -> QtWidgets.QPushButton:
    btn = QtWidgets.QPushButton()
    btn.setFixedSize(btn_size, btn_size)
    btn.setFlat(True)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    btn.setToolTip(tooltip)
    btn.setStyleSheet(stylesheet)

    inner = QtWidgets.QLabel(btn)
    inner.setFixedSize(btn_size, btn_size)
    inner.setAlignment(QtCore.Qt.AlignCenter)
    inner.setStyleSheet("background: transparent; border: none;")
    inner.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    px = QtGui.QPixmap(icon_path)
    if not px.isNull():
        inner.setPixmap(
            px.scaled(icon_size, icon_size,
                      QtCore.Qt.KeepAspectRatio,
                      QtCore.Qt.SmoothTransformation))
    else:
        inner.setText("♻" if "restore" in icon_path else "🗑")
        inner.setStyleSheet(
            "background: transparent; border: none; "
            "color: #fff; font: 16pt 'Segoe UI';")

    return btn


# ── Shadow-painting central widget ───────────────────────────────────────────
class _ShadowWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, shadow_inset=18, bg="#F4FAF7", corner_r=10):
        super().__init__(parent)
        self._si        = shadow_inset
        self._bg        = bg
        self._corner_r  = corner_r
        self.__opacity  = 0.0
        self.setAttribute(QtCore.Qt.WA_StyledBackground, False)
        self.setStyleSheet("background: transparent;")

    def _get_opacity(self) -> float:
        return self.__opacity

    def _set_opacity(self, val: float):
        self.__opacity = max(0.0, min(1.0, val))
        self.update()

    cardOpacity = pyqtProperty(float, _get_opacity, _set_opacity)

    def paintEvent(self, event):
        if self.__opacity <= 0:
            return

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setOpacity(self.__opacity)

        si   = self._si
        card = self.rect().adjusted(si, si, -si, -si)

        for spread, alpha in [(16, 0.05), (12, 0.07), (8, 0.09), (4, 0.11), (2, 0.08)]:
            sr = card.adjusted(-spread // 4, spread // 3, spread // 4, spread)
            path = QtGui.QPainterPath()
            path.addRoundedRect(float(sr.x()), float(sr.y()),
                                float(sr.width()), float(sr.height()),
                                float(self._corner_r + 2), float(self._corner_r + 2))
            p.setBrush(QtGui.QColor(27, 67, 50, int(alpha * 255)))
            p.setPen(QtCore.Qt.NoPen)
            p.drawPath(path)

        card_path = QtGui.QPainterPath()
        card_path.addRoundedRect(float(card.x()), float(card.y()),
                                 float(card.width()), float(card.height()),
                                 float(self._corner_r), float(self._corner_r))
        p.setBrush(QtGui.QColor(self._bg))
        p.setPen(QtGui.QPen(QtGui.QColor("#E0EDE6"), 0.8))
        p.drawPath(card_path)
        p.end()


# ── Apple-style open-animation mixin ─────────────────────────────────────────
class _OpenAnimMixin:
    _DURATION   = 340
    _SCALE_FROM = 0.94

    def play_open_animation(self, shadow_widget: _ShadowWidget):
        geo = self.geometry()
        cx, cy = geo.center().x(), geo.center().y()
        sw = int(geo.width()  * self._SCALE_FROM)
        sh = int(geo.height() * self._SCALE_FROM)
        start_geo = QtCore.QRect(cx - sw // 2, cy - sh // 2, sw, sh)

        self._anim_geo = QPropertyAnimation(self, b"geometry")
        self._anim_geo.setDuration(self._DURATION)
        self._anim_geo.setStartValue(start_geo)
        self._anim_geo.setEndValue(geo)
        self._anim_geo.setEasingCurve(QEasingCurve.OutBack)

        self._anim_fade = QPropertyAnimation(shadow_widget, b"cardOpacity")
        self._anim_fade.setDuration(self._DURATION - 60)
        self._anim_fade.setStartValue(0.0)
        self._anim_fade.setEndValue(1.0)
        self._anim_fade.setEasingCurve(QEasingCurve.OutCubic)

        self._anim_group = QParallelAnimationGroup(self)
        self._anim_group.addAnimation(self._anim_geo)
        self._anim_group.addAnimation(self._anim_fade)
        self._anim_group.start()


# ── Main UI class ─────────────────────────────────────────────────────────────
class Ui_RecycleBin(object):

    def setupUi(self, RecycleBin):
        RecycleBin.setObjectName("RecycleBin")
        RecycleBin.setMinimumSize(1100, 700)
        RecycleBin.resize(1200, 780)

        RecycleBin.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        RecycleBin.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        RecycleBin.setStyleSheet("QMainWindow { background: transparent; }")

        _SI = 18

        self._shadow_widget = _ShadowWidget(
            RecycleBin, shadow_inset=_SI, bg=_BG, corner_r=10)
        RecycleBin.setCentralWidget(self._shadow_widget)

        root = QtWidgets.QVBoxLayout(self._shadow_widget)
        root.setContentsMargins(_SI, _SI, _SI, _SI)
        root.setSpacing(0)

        # ── Title bar ─────────────────────────────────────────────────────────
        self.titleBar = QtWidgets.QFrame()
        self.titleBar.setObjectName("titleBar")
        self.titleBar.setFixedHeight(64)
        self.titleBar.setStyleSheet(
            f"QFrame#titleBar {{ background: {_HEADER_BG}; }}")

        tb_h = QtWidgets.QHBoxLayout(self.titleBar)
        tb_h.setContentsMargins(16, 0, 0, 0)
        tb_h.setSpacing(10)

        # Icon pill
        icon_pill = QtWidgets.QLabel()
        icon_pill.setFixedSize(44, 44)
        icon_pill.setAlignment(QtCore.Qt.AlignCenter)
        icon_pill.setStyleSheet(
            "background: rgba(255,255,255,0.12); border-radius: 10px; border: none;")
        rb_px = QtGui.QPixmap(f"{image_path}/Recycle Bin.png")
        if not rb_px.isNull():
            icon_pill.setPixmap(
                rb_px.scaled(26, 26, QtCore.Qt.KeepAspectRatio,
                             QtCore.Qt.SmoothTransformation))
        else:
            icon_pill.setText("🗑")
            icon_pill.setStyleSheet(
                icon_pill.styleSheet() + "font: 17pt 'Segoe UI'; color: #fff;")
        tb_h.addWidget(icon_pill)

        # Title + subtitle
        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(1)
        title_col.setContentsMargins(0, 0, 0, 0)

        h_title = QtWidgets.QLabel("Recycle Bin")
        h_title.setStyleSheet(
            "color: #fff; font: 700 11pt 'Segoe UI'; "
            "background: transparent; border: none; letter-spacing: 0.3px;")

        h_sub = QtWidgets.QLabel("Restore or permanently delete trashed records")
        h_sub.setStyleSheet(
            "color: rgba(198,246,213,0.55); font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")

        title_col.addWidget(h_title)
        title_col.addWidget(h_sub)
        tb_h.addLayout(title_col)
        tb_h.addStretch()

        # Action buttons
        self.Restore_btn = _icon_action_btn(
            icon_path  = f"{image_path}/restore.png",
            stylesheet = _RESTORE_BTN_SS,
            tooltip    = "Restore selected records",
            icon_size  = 26,
            btn_size   = 44,
        )
        self.Restore_btn.setObjectName("Restore_btn")

        self.Delete_permanently_btn = _icon_action_btn(
            icon_path  = f"{image_path}/hard-delete.png",
            stylesheet = _DELETE_BTN_SS,
            tooltip    = "Delete selected records permanently",
            icon_size  = 26,
            btn_size   = 44,
        )
        self.Delete_permanently_btn.setObjectName("Delete_permanently_btn")

        tb_h.addWidget(self.Restore_btn)
        tb_h.addSpacing(6)
        tb_h.addWidget(self.Delete_permanently_btn)
        tb_h.addSpacing(6)

        # Caption controls
        self._minimizeBtn = _caption_btn("—")
        self._minimizeBtn.setToolTip("Minimize")
        self._maximizeBtn = _caption_btn("⬜")
        self._maximizeBtn.setToolTip("Maximize / Restore")
        self._closeBtn    = _caption_btn("✕", close=True)
        self._closeBtn.setToolTip("Close")

        tb_h.addWidget(self._minimizeBtn)
        tb_h.addWidget(self._maximizeBtn)
        tb_h.addWidget(self._closeBtn)

        root.addWidget(self.titleBar)

        # Accent line
        accent = QtWidgets.QFrame()
        accent.setFixedHeight(2)
        accent.setStyleSheet(f"background: {_G200}; border: none;")
        root.addWidget(accent)

        # ── Body ──────────────────────────────────────────────────────────────
        body = QtWidgets.QWidget()
        body.setStyleSheet(f"background: {_BG};")
        body_lay = QtWidgets.QVBoxLayout(body)
        body_lay.setContentsMargins(18, 16, 18, 14)
        body_lay.setSpacing(12)

        sec_lbl = QtWidgets.QLabel("TRASHED RECORDS")
        sec_lbl.setStyleSheet(_LABEL_MUTED_SS)
        body_lay.addWidget(sec_lbl)

        # Table card
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            f"QFrame {{ background: {_SURFACE}; "
            f"border: 1px solid {_BORDER}; border-radius: 10px; }}")
        card_lay = QtWidgets.QVBoxLayout(card)
        card_lay.setContentsMargins(0, 0, 0, 0)
        card_lay.setSpacing(0)

        self.recycle_table = QtWidgets.QTableWidget()
        self.recycle_table.setObjectName("recycle_table")
        self.recycle_table.setStyleSheet(_TABLE_SS)
        self.recycle_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recycle_table.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.recycle_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.recycle_table.setWordWrap(True)
        self.recycle_table.setAlternatingRowColors(True)
        self.recycle_table.setShowGrid(True)

        self.recycle_table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.recycle_table.verticalHeader().setDefaultSectionSize(52)
        self.recycle_table.horizontalHeader().setStretchLastSection(True)
        self.recycle_table.horizontalHeader().setDefaultSectionSize(200)

        self.recycle_table.setColumnCount(9)
        for col, (lbl, w) in enumerate([
            ("",                 0  ),
            ("Category",         110),
            ("Admin",            120),
            ("Date",             100),
            ("Client",           160),
            ("Time",             230),
            ("Chemicals Used",   260),
            ("Actual Chemicals", 260),
            ("Remarks",          220),
        ]):
            item = QtWidgets.QTableWidgetItem(lbl)
            item.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
            self.recycle_table.setHorizontalHeaderItem(col, item)
            if w:
                self.recycle_table.setColumnWidth(col, w)

        self.recycle_table.setColumnHidden(0, True)

        card_lay.addWidget(self.recycle_table)
        body_lay.addWidget(card, 1)
        root.addWidget(body, 1)

        self._install_drag(RecycleBin)
        self.retranslateUi(RecycleBin)
        QtCore.QMetaObject.connectSlotsByName(RecycleBin)

    def _install_drag(self, window):
        self._drag_pos = None

        def _press(e):
            if e.button() == QtCore.Qt.LeftButton:
                self._drag_pos = e.globalPos() - window.frameGeometry().topLeft()

        def _move(e):
            if e.buttons() == QtCore.Qt.LeftButton and self._drag_pos is not None:
                window.move(e.globalPos() - self._drag_pos)

        def _release(e):
            self._drag_pos = None

        self.titleBar.mousePressEvent   = _press
        self.titleBar.mouseMoveEvent    = _move
        self.titleBar.mouseReleaseEvent = _release

        self._closeBtn.clicked.connect(window.close)
        self._minimizeBtn.clicked.connect(window.showMinimized)
        self._maximizeBtn.clicked.connect(
            lambda: window.showNormal()
            if window.isMaximized() else window.showMaximized())

    def retranslateUi(self, RecycleBin):
        RecycleBin.setWindowTitle(
            QtCore.QCoreApplication.translate("RecycleBin", "Recycle Bin"))


# ── Concrete window with built-in open animation ──────────────────────────────
class RecycleBinWindow(QtWidgets.QMainWindow, _OpenAnimMixin):
    """
    Drop-in QMainWindow replacement. Call show_animated() instead of show().
    """

    def show_animated(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.center().x() - self.width()  // 2,
            screen.center().y() - self.height() // 2,
        )
        self.show()
        QTimer.singleShot(0, self._kick_animation)

    def _kick_animation(self):
        sw = getattr(self, "_ui_ref", None) or self.centralWidget()
        self.play_open_animation(sw)

    def set_ui(self, ui: "Ui_RecycleBin"):
        self._ui_ref = ui._shadow_widget


# ── Standalone preview ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Install custom tooltips — completely replaces Qt's native tooltip
    # rendering so it works perfectly on frameless/translucent windows
    install_custom_tooltips(app)

    win = RecycleBinWindow()
    ui = Ui_RecycleBin()
    ui.setupUi(win)
    win.set_ui(ui)
    win.show_animated()

    sys.exit(app.exec_())