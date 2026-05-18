# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QTableWidgetItem, QWidget, QDialog, QApplication,
    QHBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QLabel, QTableWidget,
    QVBoxLayout, QHeaderView, QAbstractItemView, QStyledItemDelegate,
    QPushButton, QFrame, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import (
    Qt, QSize, QPoint, QRect, QEvent, QTimer,
    QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    pyqtProperty
)
from PyQt5.QtGui import (
    QFont, QColor, QPainter, QPainterPath, QPen, QRegion,
    QFontMetrics, QCursor
)


# ══════════════════════════════════════════════════════════════════════════════
#  Theme tokens
# ══════════════════════════════════════════════════════════════════════════════
_CLR_BG          = "#F0FAF4"
_CLR_PRIMARY     = "#2F6B3F"
_CLR_PRIMARY_DK  = "#1B4332"
_CLR_PRIMARY_XDK = "#0D2B1A"
_CLR_ACCENT      = "#C6F6D5"
_CLR_TEXT        = "#1B4332"
_CLR_BORDER      = "#A8D5BA"
_CLR_GRID        = "#D6EDE0"
_CLR_SURFACE     = "#FFFFFF"
_CLR_SURFACE_2   = "#EDF7F1"
_CLR_DANGER      = "#B91C1C"
_CLR_DANGER_BG   = "#FEF2F2"

_FONT            = "'SF Pro Text', '.AppleSystemUIFont', 'Segoe UI', sans-serif"
_FONT_DISPLAY    = "'SF Pro Display', '.AppleSystemUIFont', 'Segoe UI Semibold', sans-serif"
_CORNER_R        = 12
_SHADOW_INSET    = 18


# ══════════════════════════════════════════════════════════════════════════════
#  Custom tooltip — fully painted, works on frameless / translucent windows
# ══════════════════════════════════════════════════════════════════════════════
class _CustomTooltip(QWidget):
    _instance = None

    def __init__(self):
        super().__init__(None, Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setWindowFlags(
            Qt.ToolTip
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.BypassGraphicsProxyWidget
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
        fm = QFontMetrics(QFont("Segoe UI", 9))
        text_rect = fm.boundingRect(text)
        pad_x, pad_y = 14, 8
        w = text_rect.width()  + pad_x * 2
        h = text_rect.height() + pad_y * 2
        self.setFixedSize(w, h)

        screen = QApplication.screenAt(global_pos)
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
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.5, 0.5,
                            self.width() - 1, self.height() - 1, 6, 6)
        p.setBrush(QColor("#FFFFFF"))
        p.setPen(QPen(QColor("#A8D5BA"), 1.0))
        p.drawPath(path)
        p.setPen(QColor("#1B4332"))
        p.setFont(QFont("Segoe UI", 9))
        p.drawText(self.rect(), Qt.AlignCenter, self._text)
        p.end()


class _TooltipFilter:
    """
    Mixin-style event filter — install on a QDialog to intercept ToolTip
    events and show our custom white tooltip instead of the black native one.
    """
    @staticmethod
    def install_on(widget: QWidget):
        f = _TooltipEventFilter(widget)
        widget.installEventFilter(f)
        widget._tooltip_filter = f  # prevent GC


class _TooltipEventFilter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            widget = obj
            if isinstance(widget, QWidget) and widget.toolTip():
                _CustomTooltip.instance().show_tip(
                    event.globalPos(), widget.toolTip())
            return True
        if event.type() == QEvent.Leave:
            _CustomTooltip.instance().hide()
        return False


def install_custom_tooltips(app_or_widget):
    """
    Install custom tooltips on a QApplication (global) or a single QWidget.
    """
    f = _TooltipEventFilter(app_or_widget)
    app_or_widget.installEventFilter(f)
    app_or_widget._tooltip_filter = f


# ══════════════════════════════════════════════════════════════════════════════
#  Shared style strings
# ══════════════════════════════════════════════════════════════════════════════
_INPUT_SS = f"""
QLineEdit {{
    background: {_CLR_SURFACE};
    border: 1.5px solid {_CLR_BORDER};
    border-radius: 7px;
    padding: 6px 12px;
    font: 13px {_FONT};
    color: {_CLR_TEXT};
    min-height: 32px;
    selection-background-color: {_CLR_ACCENT};
    selection-color: {_CLR_TEXT};
}}
QLineEdit:focus {{
    border: 1.5px solid {_CLR_PRIMARY};
    background: {_CLR_SURFACE};
}}
"""

_COMBO_SS = f"""
QComboBox {{
    background: {_CLR_SURFACE};
    border: 1.5px solid {_CLR_BORDER};
    border-radius: 7px;
    padding: 4px 10px;
    font: 13px {_FONT};
    color: {_CLR_TEXT};
    min-height: 32px;
    selection-background-color: {_CLR_ACCENT};
    selection-color: {_CLR_TEXT};
}}
QComboBox:focus {{ border: 1.5px solid {_CLR_PRIMARY}; }}
QComboBox::drop-down {{
    border: none;
    width: 26px;
    background: transparent;
    subcontrol-origin: padding;
    subcontrol-position: top right;
}}
QComboBox::down-arrow {{ width: 10px; height: 10px; }}
QComboBox QAbstractItemView {{
    background: {_CLR_SURFACE};
    border: 1.5px solid {_CLR_BORDER};
    border-radius: 7px;
    padding: 4px;
    outline: none;
    font: 13px {_FONT};
    color: {_CLR_TEXT};
    selection-background-color: {_CLR_ACCENT};
    selection-color: {_CLR_TEXT};
    min-width: 80px;
}}
"""

_LISTVIEW_SS = f"""
QListView {{
    background: {_CLR_SURFACE};
    color: {_CLR_TEXT};
    font: 13px {_FONT};
    border: none;
    outline: none;
    padding: 4px;
}}
QListView::item {{
    padding: 5px 10px;
    min-height: 26px;
    background: {_CLR_SURFACE};
    color: {_CLR_TEXT};
}}
QListView::item:hover    {{ background: {_CLR_SURFACE_2}; }}
QListView::item:selected {{ background: {_CLR_ACCENT}; color: {_CLR_TEXT}; }}
"""

_EDITOR_SS = f"""
QLineEdit {{
    font: 13px {_FONT};
    padding: 5px 8px;
    border: 1.5px solid {_CLR_PRIMARY};
    border-radius: 5px;
    background: {_CLR_SURFACE};
    color: {_CLR_TEXT};
    min-height: 32px;
}}
QLineEdit:focus {{ border-color: {_CLR_PRIMARY_DK}; }}
"""

_TABLE_SS = f"""
QTableWidget {{
    background: {_CLR_SURFACE};
    border: none;
    gridline-color: {_CLR_GRID};
    font: 13px {_FONT};
    color: {_CLR_TEXT};
    alternate-background-color: {_CLR_BG};
}}
QTableWidget::item {{
    padding: 6px 10px;
    color: {_CLR_TEXT};
    border: none;
}}
QTableWidget::item:selected {{
    background-color: {_CLR_ACCENT};
    color: {_CLR_TEXT};
}}
QHeaderView::section {{
    background-color: {_CLR_PRIMARY};
    color: #FFFFFF;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid {_CLR_PRIMARY_DK};
    font: bold 11px {_FONT};
    letter-spacing: 0.4px;
}}
QHeaderView::section:last {{ border-right: none; }}
QScrollBar:vertical {{
    background: transparent; width: 8px;
}}
QScrollBar::handle:vertical {{
    background: {_CLR_ACCENT}; border-radius: 4px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: {_CLR_BORDER}; }}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}
"""

_FIELD_LBL_SS = f"""
QLabel {{
    font: 13px {_FONT};
    color: #4A6655;
    background: transparent;
}}
"""

_SECTION_LBL_SS = f"""
QLabel {{
    font: bold 10px {_FONT};
    color: {_CLR_PRIMARY};
    background: transparent;
    letter-spacing: 0.8px;
}}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  Windows-style title-bar controls — full-height (matches recycle bin)
# ══════════════════════════════════════════════════════════════════════════════
class _WinControlBtn(QPushButton):
    _STYLE = """
        QPushButton {{
            background: transparent;
            border: none;
            color: {fg};
            font: 10pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Segoe UI', sans-serif;
            min-width: 46px;
            min-height: {h}px;
            max-height: {h}px;
        }}
        QPushButton:hover   {{ background: {hbg}; color: {hfg}; }}
        QPushButton:pressed {{ background: {pbg}; color: {hfg}; }}
    """

    def __init__(self, glyph: str, role: str, bar_height: int = 52, parent=None):
        super().__init__(glyph, parent)
        fg = "rgba(255,255,255,0.75)"
        if role == "close":
            self.setStyleSheet(self._STYLE.format(
                fg=fg, hbg="#C42B1C", hfg="#FFFFFF", pbg="#A31C12", h=bar_height))
        else:
            self.setStyleSheet(self._STYLE.format(
                fg=fg,
                hbg="rgba(255,255,255,0.13)",
                hfg="#FFFFFF",
                pbg="rgba(255,255,255,0.22)",
                h=bar_height))
        self.setFixedSize(46, bar_height)
        self.setFlat(True)
        self.setCursor(QCursor(Qt.ArrowCursor))


# ══════════════════════════════════════════════════════════════════════════════
#  Title bar
# ══════════════════════════════════════════════════════════════════════════════
_TITLE_BAR_H = 52

class _TitleBar(QWidget):

    def __init__(self, dialog: "EditRecordDialog"):
        super().__init__(dialog)
        self._dialog   = dialog
        self._drag_pos = None
        self.setFixedHeight(_TITLE_BAR_H)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2F6B3F, stop:1 #245432
                );
            }}
        """)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(18, 0, 0, 0)
        lay.setSpacing(0)

        pip = QFrame()
        pip.setFixedSize(4, 28)
        pip.setStyleSheet(
            "background: rgba(255,255,255,0.35); border-radius: 2px;")
        lay.addWidget(pip)
        lay.addSpacing(12)

        col = QVBoxLayout()
        col.setSpacing(1)
        col.setContentsMargins(0, 0, 0, 0)

        t = QLabel("Edit Record Data")
        t.setStyleSheet(f"""
            QLabel {{
                font: bold 13px {_FONT_DISPLAY};
                color: #FFFFFF;
                background: transparent;
                border: transparent;
            }}
        """)
        s = QLabel("Update the fields below and press Save Changes")
        s.setStyleSheet(f"""
            QLabel {{
                font: 11px {_FONT};
                color: rgba(255,255,255,0.60);
                background: transparent;
                border: transparent;
            }}
        """)
        col.addWidget(t)
        col.addWidget(s)
        lay.addLayout(col)
        lay.addStretch()

        # Full-height caption buttons (same style as recycle bin)
        self._btn_min   = _WinControlBtn("—",  "min",   _TITLE_BAR_H)
        self._btn_max   = _WinControlBtn("⬜", "max",   _TITLE_BAR_H)
        self._btn_close = _WinControlBtn("✕",  "close", _TITLE_BAR_H)

        self._btn_min.setToolTip("Minimize")
        self._btn_max.setToolTip("Maximize / Restore")
        self._btn_close.setToolTip("Close")

        self._btn_min.clicked.connect(dialog.showMinimized)
        self._btn_max.clicked.connect(
            lambda: dialog.showNormal() if dialog.isMaximized()
            else dialog.showMaximized())
        self._btn_close.clicked.connect(dialog.reject)

        lay.addWidget(self._btn_min)
        lay.addWidget(self._btn_max)
        lay.addWidget(self._btn_close)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = (
                e.globalPos() - self._dialog.frameGeometry().topLeft())

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self._dialog.move(e.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, _):
        self._drag_pos = None

    def mouseDoubleClickEvent(self, _):
        if self._dialog.isMaximized():
            self._dialog.showNormal()
        else:
            self._dialog.showMaximized()


# ══════════════════════════════════════════════════════════════════════════════
#  Inline table editor
# ══════════════════════════════════════════════════════════════════════════════
class _TallEditor(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        ed = QLineEdit(parent)
        ed.setMinimumHeight(36)
        ed.setStyleSheet(_EDITOR_SS)
        return ed


# ══════════════════════════════════════════════════════════════════════════════
#  Small helpers
# ══════════════════════════════════════════════════════════════════════════════
def _hline() -> QFrame:
    ln = QFrame()
    ln.setFrameShape(QFrame.HLine)
    ln.setFixedHeight(1)
    ln.setStyleSheet(f"background: {_CLR_GRID}; border: none;")
    return ln


def _section_label(text: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setStyleSheet(_SECTION_LBL_SS)
    return lbl


def _field_label(text: str, width: int = 90) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(_FIELD_LBL_SS)
    lbl.setFixedWidth(width)
    return lbl


# ══════════════════════════════════════════════════════════════════════════════
#  Main dialog
# ══════════════════════════════════════════════════════════════════════════════
class EditRecordDialog(QDialog):

    MONTHS   = [str(i) for i in range(1, 13)]
    DATES    = [str(i) for i in range(1, 32)]
    YEARS    = [str(i) for i in range(2015, 2030)]
    HOURS    = [str(i) for i in range(1, 13)]
    MINUTES  = [f"{i:02d}" for i in range(0, 60)]
    MERIDIEM = ["AM", "PM"]

    # ── Animation constants ───────────────────────────────────────────────────
    _ANIM_DURATION = 340
    _ANIM_SCALE    = 0.94

    def __init__(self, record: dict, parent=None):
        super().__init__(parent)
        self.record = record

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setMinimumWidth(730 + _SHADOW_INSET * 2)
        self.setMinimumHeight(900 + _SHADOW_INSET * 2)

        # Install custom tooltips on this dialog
        install_custom_tooltips(self)

        # Opacity for open animation (starts invisible)
        self.__card_opacity = 0.0

        self._build_ui()
        self._populate()

    # ── Card opacity property for animation ───────────────────────────────────
    def _get_card_opacity(self) -> float:
        return self.__card_opacity

    def _set_card_opacity(self, val: float):
        self.__card_opacity = max(0.0, min(1.0, val))
        self.update()

    cardOpacity = pyqtProperty(float, _get_card_opacity, _set_card_opacity)

    # ── Apple-style open animation ────────────────────────────────────────────
    def show_animated(self):
        """Show with macOS-style scale-up + fade-in animation."""
        # Centre on screen or parent
        if self.parent():
            pg = self.parent().geometry()
            cx = pg.center().x() - self.width() // 2
            cy = pg.center().y() - self.height() // 2
        else:
            screen = QApplication.primaryScreen().availableGeometry()
            cx = screen.center().x() - self.width() // 2
            cy = screen.center().y() - self.height() // 2
        self.move(cx, cy)
        self.show()
        QTimer.singleShot(0, self._run_open_animation)

    def _run_open_animation(self):
        geo = self.geometry()
        cx, cy = geo.center().x(), geo.center().y()
        sw = int(geo.width()  * self._ANIM_SCALE)
        sh = int(geo.height() * self._ANIM_SCALE)
        start_geo = QRect(cx - sw // 2, cy - sh // 2, sw, sh)

        # Scale spring
        self._anim_geo = QPropertyAnimation(self, b"geometry")
        self._anim_geo.setDuration(self._ANIM_DURATION)
        self._anim_geo.setStartValue(start_geo)
        self._anim_geo.setEndValue(geo)
        self._anim_geo.setEasingCurve(QEasingCurve.OutBack)

        # Fade in
        self._anim_fade = QPropertyAnimation(self, b"cardOpacity")
        self._anim_fade.setDuration(self._ANIM_DURATION - 60)
        self._anim_fade.setStartValue(0.0)
        self._anim_fade.setEndValue(1.0)
        self._anim_fade.setEasingCurve(QEasingCurve.OutCubic)

        self._anim_group = QParallelAnimationGroup(self)
        self._anim_group.addAnimation(self._anim_geo)
        self._anim_group.addAnimation(self._anim_fade)
        self._anim_group.start()

    # ── Paint: shadow + card, respects cardOpacity ────────────────────────────
    def paintEvent(self, event):
        if self.__card_opacity <= 0:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setOpacity(self.__card_opacity)

        card = self.rect().adjusted(
            _SHADOW_INSET, _SHADOW_INSET,
            -_SHADOW_INSET, -_SHADOW_INSET)

        # Multi-layer drop shadow
        for spread, alpha in [(14, 0.06), (10, 0.08), (6, 0.10), (3, 0.12), (1, 0.09)]:
            sr = card.adjusted(-spread // 4, spread // 3,
                               spread // 4, spread)
            sp = QPainterPath()
            sp.addRoundedRect(
                float(sr.x()), float(sr.y()),
                float(sr.width()), float(sr.height()),
                float(_CORNER_R + 2), float(_CORNER_R + 2))
            p.setBrush(QColor(27, 67, 50, int(alpha * 255)))
            p.setPen(Qt.NoPen)
            p.drawPath(sp)

        # Card background
        cp = QPainterPath()
        cp.addRoundedRect(
            float(card.x()), float(card.y()),
            float(card.width()), float(card.height()),
            float(_CORNER_R), float(_CORNER_R))
        p.setBrush(QColor(_CLR_BG))
        p.setPen(QPen(QColor(_CLR_BORDER), 0.8))
        p.drawPath(cp)
        p.end()

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(
            _SHADOW_INSET, _SHADOW_INSET,
            _SHADOW_INSET, _SHADOW_INSET)
        outer.setSpacing(0)

        card = QWidget()
        card.setObjectName("card")
        card.setStyleSheet(f"QWidget#card {{ background: {_CLR_BG}; }}")
        card.setAttribute(Qt.WA_StyledBackground, True)
        outer.addWidget(card)

        root = QVBoxLayout(card)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(_TitleBar(self))

        rule = QFrame()
        rule.setFrameShape(QFrame.HLine)
        rule.setFixedHeight(2)
        rule.setStyleSheet(f"background: {_CLR_PRIMARY_DK}; border: none;")
        root.addWidget(rule)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background: {_CLR_BG}; border: none; }}
            QScrollBar:vertical {{
                background: transparent; width: 8px; margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: {_CLR_ACCENT}; border-radius: 4px; min-height: 24px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {_CLR_BORDER}; }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{ height: 0; }}
        """)

        body = QWidget()
        body.setStyleSheet(f"background: {_CLR_BG};")
        body_lay = QVBoxLayout(body)
        body_lay.setContentsMargins(24, 20, 24, 20)
        body_lay.setSpacing(10)

        body_lay.addWidget(_section_label("Client Information"))
        body_lay.addWidget(_hline())

        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Enter client name…")
        self.client_input.setMinimumHeight(36)
        self.client_input.setStyleSheet(_INPUT_SS)
        body_lay.addWidget(self._field_row("Client Name", self.client_input))
        body_lay.addSpacing(6)

        body_lay.addWidget(_section_label("Date & Time"))
        body_lay.addWidget(_hline())
        body_lay.addWidget(self._field_row("Date", self._make_date_row()))
        body_lay.addSpacing(4)
        body_lay.addWidget(self._field_row("Time", self._make_time_row()))
        body_lay.addSpacing(6)

        body_lay.addWidget(_section_label("Chemicals Used"))
        body_lay.addWidget(_hline())
        self.chem_table = self._build_chem_table()
        body_lay.addWidget(self.chem_table)
        body_lay.addLayout(self._table_action_bar(self.chem_table))
        body_lay.addSpacing(10)

        body_lay.addWidget(_section_label("Actual Chemicals on Hand"))
        body_lay.addWidget(_hline())
        self.actual_table = self._build_chem_table()
        body_lay.addWidget(self.actual_table)
        body_lay.addLayout(self._table_action_bar(self.actual_table))

        scroll.setWidget(body)
        root.addWidget(scroll)

        foot_sep = QFrame()
        foot_sep.setFrameShape(QFrame.HLine)
        foot_sep.setFixedHeight(1)
        foot_sep.setStyleSheet(f"background: {_CLR_GRID}; border: none;")
        root.addWidget(foot_sep)

        footer = QWidget()
        footer.setFixedHeight(64)
        footer.setStyleSheet(f"""
            QWidget {{
                background: {_CLR_SURFACE_2};
                border-bottom-left-radius: {_CORNER_R}px;
                border-bottom-right-radius: {_CORNER_R}px;
            }}
        """)
        footer.setAttribute(Qt.WA_StyledBackground, True)
        f_lay = QHBoxLayout(footer)
        f_lay.setContentsMargins(24, 0, 24, 0)
        f_lay.setSpacing(10)
        f_lay.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedHeight(38)
        self.btn_cancel.setMinimumWidth(96)
        self.btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background: {_CLR_SURFACE};
                color: {_CLR_PRIMARY};
                border: 1.5px solid {_CLR_BORDER};
                border-radius: 8px;
                padding: 0 20px;
                font: 13px {_FONT};
            }}
            QPushButton:hover   {{ background: {_CLR_BG}; border-color: {_CLR_PRIMARY}; }}
            QPushButton:pressed {{ background: {_CLR_ACCENT}; }}
        """)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("Save Changes")
        self.btn_save.setFixedHeight(38)
        self.btn_save.setMinimumWidth(120)
        self.btn_save.setDefault(True)
        self.btn_save.setStyleSheet(f"""
            QPushButton {{
                background: {_CLR_PRIMARY};
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
                font: bold 13px {_FONT};
            }}
            QPushButton:hover   {{ background: {_CLR_PRIMARY_DK}; }}
            QPushButton:pressed {{ background: {_CLR_PRIMARY_XDK}; }}
        """)
        self.btn_save.clicked.connect(self._on_save)

        f_lay.addWidget(self.btn_cancel)
        f_lay.addWidget(self.btn_save)
        root.addWidget(footer)

    # ── Row builders ──────────────────────────────────────────────────────────
    def _field_row(self, label_text: str, widget: QWidget) -> QWidget:
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(12)
        lay.addWidget(_field_label(label_text))
        lay.addWidget(widget)
        return row

    def _make_date_row(self) -> QWidget:
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        self.month_cb = self._combo(self.MONTHS, 72)
        self.date_cb  = self._combo(self.DATES,  60)
        self.year_cb  = self._combo(self.YEARS,  90)

        for cb, lbl_text, is_last in [
            (self.month_cb, "Month", False),
            (self.date_cb,  "Day",   False),
            (self.year_cb,  "Year",  True),
        ]:
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet(
                f"font: 12px {_FONT}; color: #4A6655; background: transparent;")
            lay.addWidget(lbl)
            lay.addWidget(cb)
            if not is_last:
                sep = QFrame()
                sep.setFrameShape(QFrame.VLine)
                sep.setFixedHeight(20)
                sep.setStyleSheet(
                    f"background: {_CLR_GRID}; border: none; max-width: 1px;")
                lay.addWidget(sep, 0, Qt.AlignVCenter)
        lay.addStretch()
        return row

    def _make_time_row(self) -> QWidget:
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        self.start_h        = self._combo(self.HOURS,    54)
        self.start_m        = self._combo(self.MINUTES,  58)
        self.start_meridiem = self._combo(self.MERIDIEM, 80)
        self.end_h          = self._combo(self.HOURS,    54)
        self.end_m          = self._combo(self.MINUTES,  58)
        self.end_meridiem   = self._combo(self.MERIDIEM, 80)

        def _tag(text: str) -> QLabel:
            l = QLabel(text)
            l.setStyleSheet(
                f"font: 12px {_FONT}; color: {_CLR_PRIMARY}; background: transparent;")
            return l

        s_badge = QLabel("START")
        s_badge.setStyleSheet(f"""
            QLabel {{
                font: bold 9px {_FONT};
                color: #FFFFFF;
                background: {_CLR_PRIMARY};
                border-radius: 3px;
                padding: 2px 7px;
                letter-spacing: 0.5px;
            }}
        """)
        lay.addWidget(s_badge)
        lay.addSpacing(4)
        lay.addWidget(self.start_h)
        lay.addWidget(_tag(":"))
        lay.addWidget(self.start_m)
        lay.addWidget(self.start_meridiem)
        lay.addSpacing(14)

        arrow = QLabel("→")
        arrow.setStyleSheet(
            f"font: bold 15px; color: {_CLR_PRIMARY}; background: transparent;")
        lay.addWidget(arrow)
        lay.addSpacing(14)

        e_badge = QLabel("END")
        e_badge.setStyleSheet(f"""
            QLabel {{
                font: bold 9px {_FONT};
                color: #FFFFFF;
                background: {_CLR_PRIMARY_DK};
                border-radius: 3px;
                padding: 2px 7px;
                letter-spacing: 0.5px;
            }}
        """)
        lay.addWidget(e_badge)
        lay.addSpacing(4)
        lay.addWidget(self.end_h)
        lay.addWidget(_tag(":"))
        lay.addWidget(self.end_m)
        lay.addWidget(self.end_meridiem)
        lay.addStretch()
        return row

    def _combo(self, items, min_width: int = 70) -> QComboBox:
        cb = QComboBox()
        cb.addItems(items)
        cb.setMinimumWidth(min_width)
        cb.setStyleSheet(_COMBO_SS)
        cb.view().setStyleSheet(_LISTVIEW_SS)
        return cb

    # ── Table ─────────────────────────────────────────────────────────────────
    def _build_chem_table(self) -> QTableWidget:
        t = QTableWidget(0, 3)
        t.setHorizontalHeaderLabels(["Chemical Name", "Quantity", "Remarks"])
        t.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        t.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        t.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        t.setColumnWidth(1, 100)
        t.setSelectionMode(QAbstractItemView.SingleSelection)
        t.setWordWrap(True)
        t.setShowGrid(True)
        t.setAlternatingRowColors(True)
        t.setStyleSheet(_TABLE_SS)
        t.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        t.verticalHeader().setDefaultSectionSize(48)
        t.verticalHeader().setVisible(False)
        t.setItemDelegate(_TallEditor(t))
        return t

    def _table_action_bar(self, table: QTableWidget) -> QHBoxLayout:
        bar = QHBoxLayout()
        bar.setContentsMargins(0, 4, 0, 0)
        bar.setSpacing(8)

        add_btn = QPushButton("＋  Add Row")
        add_btn.setFixedHeight(32)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {_CLR_SURFACE_2};
                color: {_CLR_PRIMARY};
                border: 1.5px solid {_CLR_BORDER};
                border-radius: 7px;
                padding: 0 14px;
                font: bold 12px {_FONT};
            }}
            QPushButton:hover   {{ background: {_CLR_ACCENT}; border-color: {_CLR_PRIMARY}; }}
            QPushButton:pressed {{ background: {_CLR_ACCENT}; }}
        """)
        add_btn.clicked.connect(lambda: self._append_row(table))

        del_btn = QPushButton("−  Delete Row")
        del_btn.setFixedHeight(32)
        del_btn.setEnabled(False)
        del_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {_CLR_DANGER};
                border: 1.5px dashed #FECACA;
                border-radius: 7px;
                padding: 0 14px;
                font: 12px {_FONT};
            }}
            QPushButton:hover   {{ background: {_CLR_DANGER_BG}; border-color: {_CLR_DANGER}; }}
            QPushButton:pressed {{ background: #FECACA; }}
            QPushButton:disabled {{ color: #D1D5DB; border-color: {_CLR_GRID}; }}
        """)
        del_btn.clicked.connect(lambda: self._delete_row(table))
        table.itemSelectionChanged.connect(
            lambda: del_btn.setEnabled(len(table.selectedItems()) > 0))

        bar.addWidget(add_btn)
        bar.addWidget(del_btn)
        bar.addStretch()
        return bar

    def _append_row(self, table: QTableWidget):
        r = table.rowCount()
        table.insertRow(r)
        for col in range(table.columnCount()):
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            table.setItem(r, col, item)
        self._resize_table(table)
        table.scrollToBottom()
        table.setCurrentCell(r, 0)
        table.editItem(table.item(r, 0))

    def _delete_row(self, table: QTableWidget):
        row = table.currentRow()
        if row < 0:
            return
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Row")
        msg.setText("Are you sure you want to delete this row?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background: {_CLR_BG};
                font: 13px {_FONT};
                color: {_CLR_TEXT};
            }}
            QPushButton {{
                background: {_CLR_SURFACE};
                color: {_CLR_TEXT};
                border: 1px solid {_CLR_BORDER};
                border-radius: 7px;
                padding: 4px 16px;
                min-width: 72px;
                font: 13px {_FONT};
            }}
            QPushButton:default {{
                background: {_CLR_PRIMARY};
                color: #FFFFFF;
                border: none;
            }}
        """)
        if msg.exec_() == QMessageBox.Yes:
            table.removeRow(row)
            self._resize_table(table)

    def _resize_table(self, table: QTableWidget):
        row_h   = table.verticalHeader().defaultSectionSize()
        hdr_h   = table.horizontalHeader().height()
        visible = min(max(table.rowCount(), 1), 8)
        table.setFixedHeight(row_h * visible + hdr_h + 4)

    # ── Populate ──────────────────────────────────────────────────────────────
    def _populate(self):
        r = self.record
        chemicals_use    = r.get("chemicals_use")         or r.get("chemical_use")        or []
        actual_chemicals = r.get("actual_chemicals_used") or r.get("actual_chemical_used") or []

        self.client_input.setText(r.get("client_name", ""))
        self._set_combo(self.month_cb, str(r.get("month", "")))
        self._set_combo(self.date_cb,  str(r.get("date",  "")))
        self._set_combo(self.year_cb,  str(r.get("year",  "")))

        start = r.get("start_time", "01:00") or "01:00"
        end   = r.get("end_time",   "01:00") or "01:00"
        sh, sm = (start.split(":") + ["00"])[:2]
        eh, em = (end.split(":")   + ["00"])[:2]

        self._set_combo(self.start_h,        sh.lstrip("0") or "1")
        self._set_combo(self.start_m,        sm.zfill(2))
        self._set_combo(self.end_h,          eh.lstrip("0") or "1")
        self._set_combo(self.end_m,          em.zfill(2))
        self._set_combo(self.start_meridiem, r.get("start_meridiem", "AM"))
        self._set_combo(self.end_meridiem,   r.get("end_meridiem",   "AM"))

        self._fill_chem_table(self.chem_table,   chemicals_use)
        self._fill_chem_table(self.actual_table, actual_chemicals)

    def _set_combo(self, cb: QComboBox, value: str):
        idx = cb.findText(value.lstrip("0") or "0")
        if idx < 0:
            idx = cb.findText(value)
        if idx >= 0:
            cb.setCurrentIndex(idx)

    def _fill_chem_table(self, table: QTableWidget, chemicals: list):
        table.setRowCount(len(chemicals))
        for row, entry in enumerate(chemicals):
            name = (
                entry.get("chemical_name") or
                entry.get("actual_chemicals_name") or
                entry.get("name") or ""
            )
            qty     = entry.get("quantity") or entry.get("qty") or ""
            remarks = entry.get("remarks") or ""
            for col, val in enumerate([name, qty, remarks]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                table.setItem(row, col, item)
        self._resize_table(table)

    # ── Save ──────────────────────────────────────────────────────────────────
    def _on_save(self):
        client = self.client_input.text().strip()
        if not client:
            QMessageBox.warning(self, "Validation", "Client name is required.")
            return

        self.record["client_name"]           = client
        self.record["month"]                 = int(self.month_cb.currentText())
        self.record["date"]                  = int(self.date_cb.currentText())
        self.record["year"]                  = int(self.year_cb.currentText())
        self.record["start_time"]            = f"{int(self.start_h.currentText()):02d}:{self.start_m.currentText()}"
        self.record["end_time"]              = f"{int(self.end_h.currentText()):02d}:{self.end_m.currentText()}"
        self.record["start_meridiem"]        = self.start_meridiem.currentText()
        self.record["end_meridiem"]          = self.end_meridiem.currentText()
        self.record["chemicals_use"]         = self._read_chem_table(self.chem_table,   "chemical_name")
        self.record["actual_chemicals_used"] = self._read_chem_table(self.actual_table, "actual_chemicals_name")
        self.accept()

    def _read_chem_table(self, table: QTableWidget, name_key: str) -> list:
        result = []
        for row in range(table.rowCount()):
            name = table.item(row, 0).text().strip() if table.item(row, 0) else ""
            qty  = table.item(row, 1).text().strip() if table.item(row, 1) else ""
            rem  = table.item(row, 2).text().strip() if table.item(row, 2) else ""
            if name:
                result.append({name_key: name, "quantity": qty, "remarks": rem})
        return result

    def get_data(self) -> dict:
        return self.record