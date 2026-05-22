# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

base_dir   = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")

_G50  = "#F0FAF4"
_G100 = "#C6F6D5"
_G200 = "#74C69D"
_G400 = "#2D6A4F"
_G600 = "#1B4332"
_G800 = "#081C15"

_SIDEBAR_BG = "#1A3D2B"
_HEADER_BG  = _G400
_SURFACE    = "#FFFFFF"
_BG         = "#F4FAF7"
_TEXT       = _G600
_MUTED      = "#6B8F78"
_BORDER     = "#E0EDE6"

_SIDEBAR_EXPANDED  = 220
_SIDEBAR_COLLAPSED = 52

_SS_INPUT = f"""
QLineEdit {{
    background: {_SURFACE}; border: 1px solid {_BORDER};
    border-radius: 7px; padding: 0 10px;
    font: 11pt 'Segoe UI'; color: {_TEXT};
}}
QLineEdit:focus {{ border-color: {_G200}; background: #FAFFFE; }}
QLineEdit::placeholder {{ color: {_MUTED}; }}
"""

_SS_SELECT = f"""
QComboBox {{
    background: {_BG}; border: 1px solid {_BORDER};
    border-radius: 7px; padding: 0 10px;
    font: 10pt 'Segoe UI'; color: {_TEXT}; min-height: 32px;
}}
QComboBox:focus {{ border-color: {_G200}; }}
QComboBox::drop-down {{ border: none; width: 18px; }}
QComboBox QAbstractItemView {{
    background: {_SURFACE}; border: 1px solid {_BORDER};
    border-radius: 6px; selection-background-color: {_G400};
    selection-color: #fff; font: 10pt 'Segoe UI';
}}
"""

_SS_TABLE_MINI = f"""
QTableWidget {{
    background: {_SURFACE}; alternate-background-color: {_BG};
    gridline-color: {_BORDER}; border: none;
    font: 10pt 'Segoe UI'; color: {_TEXT};
    selection-background-color: {_G100}; selection-color: {_TEXT};
}}
QTableWidget::item {{ padding: 5px 8px; border: none; }}
QTableWidget::item:hover {{ background: #E8F5EE; }}
QHeaderView::section {{
    background: {_G400}; color: #fff; border: none;
    border-right: 1px solid {_G600}; padding: 6px 8px;
    font: 500 9pt 'Segoe UI';
}}
QHeaderView {{ background: transparent; border: none; }}
QTableCornerButton::section {{ background: {_G400}; border: none; }}
QScrollBar:vertical {{ background: {_BG}; width: 5px; border-radius: 2px; }}
QScrollBar::handle:vertical {{ background: {_BORDER}; border-radius: 2px; min-height: 20px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""

_SS_TABLE_MAIN = f"""
QTableWidget {{
    background: {_SURFACE}; alternate-background-color: {_BG};
    gridline-color: {_BORDER}; border: none;
    font: 10pt 'Segoe UI'; color: {_TEXT};
    selection-background-color: {_G100}; selection-color: {_TEXT};
}}
QTableWidget::item {{ padding: 8px 12px; border: none; }}
QTableWidget::item:hover {{ background: #E8F5EE; }}
QHeaderView::section {{
    background: {_G400}; color: #fff; border: none;
    border-right: 1px solid {_G600}; padding: 8px 12px;
    font: 500 10pt 'Segoe UI';
}}
QHeaderView {{ background: transparent; border: none; }}
QTableCornerButton::section {{ background: {_G400}; border: none; }}
QScrollBar:vertical {{ background: {_BG}; width: 6px; border-radius: 3px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {_G200}; border-radius: 3px; min-height: 20px; }}
QScrollBar::handle:vertical:hover {{ background: {_G400}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ background: {_BG}; height: 6px; border-radius: 3px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {_G200}; border-radius: 3px; min-width: 20px; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""

_SS_BTN_PRIMARY = f"""
QPushButton {{
    background: {_G400}; color: #fff; border: none;
    border-radius: 7px; padding: 8px 16px; font: 500 10pt 'Segoe UI';
}}
QPushButton:hover   {{ background: {_G600}; }}
QPushButton:pressed {{ background: {_G800}; }}
QPushButton:disabled {{ background: {_G100}; color: rgba(255,255,255,.5); }}
"""

_SS_BTN_DANGER = """
QPushButton {
    background: #DC2626; color: #fff; border: none;
    border-radius: 7px; padding: 8px 16px; font: 500 10pt 'Segoe UI';
}
QPushButton:hover   { background: #B91C1C; }
QPushButton:pressed { background: #991B1B; }
"""

_SS_BTN_PDF = """
QPushButton {
    background: #1D4ED8; color: #fff; border: none;
    border-radius: 7px; padding: 8px 16px; font: 500 10pt 'Segoe UI';
}
QPushButton:hover   { background: #1E40AF; }
QPushButton:pressed { background: #1E3A8A; }
"""

_SS_BTN_OUTLINE = f"""
QPushButton {{
    background: transparent; color: {_G400};
    border: 1px solid {_G400}; border-radius: 6px;
    padding: 3px 10px; font: 500 9pt 'Segoe UI';
}}
QPushButton:hover   {{ background: {_G400}; color: #fff; }}
QPushButton:pressed {{ background: {_G600}; color: #fff; }}
"""

# Nav buttons: NOT checkable — we manage active state manually via stylesheet
_SS_NAV_IDLE = f"""
QPushButton {{
    background: transparent;
    color: rgba(198,246,213,0.60);
    border: none; border-radius: 8px;
    padding: 9px 12px; text-align: left;
    font: 10pt 'Segoe UI';
}}
QPushButton:hover {{
    background: rgba(255,255,255,0.07);
    color: rgba(198,246,213,0.90);
}}
QPushButton:pressed {{
    background: rgba(255,255,255,0.10);
}}
"""

_SS_NAV_ACTIVE = f"""
QPushButton {{
    background: rgba(198,246,213,0.13);
    color: #C6F6D5; font-weight: 600;
    border: none; border-left: 3px solid {_G200}; border-radius: 8px;
    padding: 9px 12px; text-align: left;
    font: 10pt 'Segoe UI';
}}
QPushButton:hover {{
    background: rgba(198,246,213,0.18);
    color: #C6F6D5;
}}
QPushButton:pressed {{
    background: rgba(198,246,213,0.22);
}}
"""

_SS_LOGOUT_BTN = """
QPushButton {
    background: transparent; color: rgba(255,120,100,0.70);
    border: none; border-radius: 8px;
    padding: 9px 12px; text-align: left;
    font: 10pt 'Segoe UI';
}
QPushButton:hover {
    background: rgba(255,100,80,0.10);
    color: rgba(255,130,110,1.0);
}
QPushButton:pressed {
    background: rgba(255,100,80,0.15);
}
"""

_SS_SEARCH = f"""
QLineEdit {{
    background: transparent; border: none;
    font: 10pt 'Segoe UI'; color: {_TEXT};
}}
QLineEdit::placeholder {{ color: {_MUTED}; }}
"""

# Toggle button for collapsing sidebar
_SS_TOGGLE_BTN = f"""
QPushButton {{
    background: transparent;
    color: rgba(198,246,213,0.60);
    border: none; border-radius: 8px;
    font: 14pt 'Segoe UI';
}}
QPushButton:hover {{
    background: rgba(198,246,213,0.13);
    color: rgba(198,246,213,0.90);
}}
QPushButton:pressed {{
    background: rgba(198,246,213,0.22);
    color: #C6F6D5;
}}
"""

_LABEL_SECTION = (
    f"background: transparent; border: none; "
    f"color: {_MUTED}; font: 600 8pt 'Segoe UI'; letter-spacing: 1.5px;"
)
_LABEL_TIME = (
    f"background: transparent; border: none; "
    f"color: {_G400}; font: 600 9pt 'Segoe UI';"
)


# ─────────────────────────────────────────────────────────────────────────────
#  Caption buttons
# ─────────────────────────────────────────────────────────────────────────────
class CaptionButton(QtWidgets.QPushButton):
    def __init__(self, symbol: str, is_close: bool = False, parent=None):
        super().__init__(symbol, parent)
        self._is_close = is_close
        self.setFixedSize(46, 36)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setFlat(True)
        self._apply_style(hovered=False)

    def _apply_style(self, hovered: bool):
        if self._is_close:
            bg = "#C42B1C" if hovered else "transparent"
            fg = "#ffffff" if hovered else "rgba(255,255,255,0.80)"
            bg_press = "#B01F13"
        else:
            bg = "rgba(255,255,255,0.12)" if hovered else "transparent"
            fg = "#ffffff" if hovered else "rgba(255,255,255,0.70)"
            bg_press = "rgba(255,255,255,0.20)"
        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg}; color: {fg}; border: none; border-radius: 0px;
                font: 11pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Arial';
            }}
            QPushButton:pressed {{ background: {bg_press}; }}
        """)

    def enterEvent(self, e): self._apply_style(hovered=True);  super().enterEvent(e)
    def leaveEvent(self, e): self._apply_style(hovered=False); super().leaveEvent(e)


class WindowControls(QtWidgets.QWidget):
    closeClicked    = QtCore.pyqtSignal()
    minimizeClicked = QtCore.pyqtSignal()
    maximizeClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        self.minimizeBtn = CaptionButton("─", is_close=False)
        self.maximizeBtn = CaptionButton("□", is_close=False)
        self.closeBtn    = CaptionButton("✕", is_close=True)
        self.minimizeBtn.setToolTip("Minimize")
        self.maximizeBtn.setToolTip("Maximize / Restore")
        self.closeBtn.setToolTip("Close")
        self.minimizeBtn.clicked.connect(self.minimizeClicked)
        self.maximizeBtn.clicked.connect(self.maximizeClicked)
        self.closeBtn.clicked.connect(self.closeClicked)
        h.addWidget(self.minimizeBtn)
        h.addWidget(self.maximizeBtn)
        h.addWidget(self.closeBtn)
        self.setFixedSize(138, 36)


# ─────────────────────────────────────────────────────────────────────────────
#  Collapsible sidebar
# ─────────────────────────────────────────────────────────────────────────────
class CollapsibleSidebar(QtWidgets.QFrame):
    """
    Sidebar that animates between expanded (220 px) and collapsed (52 px).
    In collapsed mode only icons are visible (text hidden).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._expanded = True
        self._anim = QtCore.QPropertyAnimation(self, b"minimumWidth")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self._anim2 = QtCore.QPropertyAnimation(self, b"maximumWidth")
        self._anim2.setDuration(200)
        self._anim2.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.setFixedWidth(_SIDEBAR_EXPANDED)
        self.setStyleSheet(
            f"QFrame#sidebar {{ background: {_SIDEBAR_BG}; "
            "border-right: 1px solid rgba(0,0,0,0.15); }}")

    def toggle(self):
        self._expanded = not self._expanded
        target = _SIDEBAR_EXPANDED if self._expanded else _SIDEBAR_COLLAPSED
        for anim, prop in [(self._anim, b"minimumWidth"), (self._anim2, b"maximumWidth")]:
            anim.stop()
            anim.setStartValue(self.width())
            anim.setEndValue(target)
            anim.start()

    @property
    def is_expanded(self):
        return self._expanded


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _nav_btn(label: str, icon_path: str = "") -> QtWidgets.QPushButton:
    """Non-checkable nav button — active state handled via stylesheet swap."""
    btn = QtWidgets.QPushButton(f"   {label}")
    btn.setCheckable(False)
    btn.setStyleSheet(_SS_NAV_IDLE)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    btn.setFixedHeight(38)
    btn.setProperty("label", label)
    btn.setToolTip(label)
    if icon_path and os.path.exists(icon_path):
        btn.setIcon(QtGui.QIcon(icon_path))
        btn.setIconSize(QtCore.QSize(36, 36))
    return btn


def _section_div(text: str) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget()
    w.setStyleSheet("background: transparent; border: none;")
    w.setFixedHeight(26)
    h = QtWidgets.QHBoxLayout(w)
    h.setContentsMargins(0, 6, 0, 0)
    h.setSpacing(8)
    lbl = QtWidgets.QLabel(text)
    lbl.setStyleSheet(_LABEL_SECTION)
    h.addWidget(lbl)
    line = QtWidgets.QFrame()
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setStyleSheet(
        f"color: {_BORDER}; background: {_BORDER}; border: none; max-height: 1px;")
    h.addWidget(line)
    return w


def _nav_section_lbl(text: str) -> QtWidgets.QLabel:
    lbl = QtWidgets.QLabel(text)
    lbl.setContentsMargins(16, 12, 0, 4)
    lbl.setStyleSheet(
        "color: rgba(198,246,213,0.32); font: 600 7pt 'Segoe UI'; "
        "letter-spacing: 1.8px; background: transparent; border: none;")
    return lbl


# ─────────────────────────────────────────────────────────────────────────────
#  Treatment page
# ─────────────────────────────────────────────────────────────────────────────
def _build_treatment_page(ui) -> QtWidgets.QWidget:
    page = QtWidgets.QWidget()
    page.setStyleSheet(f"background: {_BG};")
    page_v = QtWidgets.QVBoxLayout(page)
    page_v.setContentsMargins(0, 0, 0, 0)
    page_v.setSpacing(0)

    action_bar = QtWidgets.QFrame()
    action_bar.setFixedHeight(48)
    action_bar.setStyleSheet(
        f"QFrame {{ background: {_SURFACE}; border-bottom: 1px solid {_BORDER}; }}")
    ab_h = QtWidgets.QHBoxLayout(action_bar)
    ab_h.setContentsMargins(16, 0, 16, 0)
    ab_h.setSpacing(10)

    search_wrap = QtWidgets.QFrame()
    search_wrap.setFixedHeight(32)
    search_wrap.setStyleSheet(
        f"QFrame {{ background: {_BG}; border: 1px solid {_BORDER}; border-radius: 8px; }}")
    sw_h = QtWidgets.QHBoxLayout(search_wrap)
    sw_h.setContentsMargins(8, 0, 8, 0)
    sw_h.setSpacing(6)

    ui.searchIcon = QtWidgets.QLabel()
    ui.searchIcon.setObjectName("searchIcon")
    ui.searchIcon.setFixedSize(16, 16)
    ui.searchIcon.setStyleSheet("background: transparent; border: none;")
    src_px = QtGui.QPixmap(f"{image_path}/searchIcon.png")
    if not src_px.isNull():
        ui.searchIcon.setPixmap(
            src_px.scaled(16, 16, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
    sw_h.addWidget(ui.searchIcon)

    ui.searchDate = QtWidgets.QLineEdit()
    ui.searchDate.setObjectName("searchDate")
    ui.searchDate.setPlaceholderText("Search client or date…")
    ui.searchDate.setStyleSheet(_SS_SEARCH)
    sw_h.addWidget(ui.searchDate)
    search_wrap.setFixedWidth(260)
    ab_h.addWidget(search_wrap)
    ab_h.addStretch()

    ui.confirmButton_2 = QtWidgets.QPushButton("  Convert to PDF")
    ui.confirmButton_2.setObjectName("confirmButton_2")
    ui.confirmButton_2.setFixedHeight(32)
    ui.confirmButton_2.setStyleSheet(_SS_BTN_PDF)
    ui.confirmButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    pdf_px = QtGui.QPixmap(f"{image_path}/PDF.png")
    if not pdf_px.isNull():
        ui.confirmButton_2.setIcon(QtGui.QIcon(pdf_px))
        ui.confirmButton_2.setIconSize(QtCore.QSize(16, 16))
    ab_h.addWidget(ui.confirmButton_2)

    ui.confirmButton_3 = QtWidgets.QPushButton("  Trash")
    ui.confirmButton_3.setObjectName("confirmButton_3")
    ui.confirmButton_3.setFixedHeight(32)
    ui.confirmButton_3.setStyleSheet(_SS_BTN_DANGER)
    ui.confirmButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    tr_px = QtGui.QPixmap(f"{image_path}/trashIcon.png")
    if not tr_px.isNull():
        ui.confirmButton_3.setIcon(QtGui.QIcon(tr_px))
        ui.confirmButton_3.setIconSize(QtCore.QSize(16, 16))
    ab_h.addWidget(ui.confirmButton_3)
    page_v.addWidget(action_bar)

    cols = QtWidgets.QHBoxLayout()
    cols.setContentsMargins(0, 0, 0, 0)
    cols.setSpacing(0)

    form_scroll = QtWidgets.QScrollArea()
    form_scroll.setWidgetResizable(True)
    form_scroll.setFixedWidth(480)
    form_scroll.setSizePolicy(
        QtWidgets.QSizePolicy.Fixed,
        QtWidgets.QSizePolicy.Expanding
    )
    form_scroll.setStyleSheet(f"""
        QScrollArea {{ background: {_SURFACE}; border: none; border-right: 1px solid {_BORDER}; }}
        QScrollBar:vertical {{ background: {_BG}; width: 5px; border-radius: 2px; }}
        QScrollBar::handle:vertical {{ background: {_BORDER}; border-radius: 2px; min-height: 20px; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    """)

    form_inner = QtWidgets.QWidget()
    form_inner.setStyleSheet(f"background: {_SURFACE};")
    form_v = QtWidgets.QVBoxLayout(form_inner)
    form_v.setContentsMargins(16, 16, 16, 16)
    form_v.setSpacing(10)

    ui.nameLabel = QtWidgets.QLabel("CLIENT NAME")
    ui.nameLabel.setObjectName("nameLabel")
    ui.nameLabel.setStyleSheet(_LABEL_SECTION)
    form_v.addWidget(ui.nameLabel)
    ui.nameofClientinput = QtWidgets.QLineEdit()
    ui.nameofClientinput.setObjectName("nameofClientinput")
    ui.nameofClientinput.setFixedHeight(34)
    ui.nameofClientinput.setPlaceholderText("e.g. Eorico")
    ui.nameofClientinput.setStyleSheet(_SS_INPUT)
    form_v.addWidget(ui.nameofClientinput)

 
    ui.dateLabel = QtWidgets.QLabel("DATE OF TREATMENT")
    ui.dateLabel.setObjectName("dateLabel")
    ui.dateLabel.setStyleSheet(_LABEL_SECTION)
    form_v.addWidget(ui.dateLabel)

    date_row = QtWidgets.QHBoxLayout()
    date_row.setSpacing(6)
    for attr, lbl_txt, items in [
        ("month", "Month", [str(i) for i in range(1, 13)]),
        ("date",  "Day",   [str(i) for i in range(1, 32)]),
        ("year",  "Year",  [str(y) for y in range(2015, 2032)]),
    ]:
        col = QtWidgets.QVBoxLayout()
        col.setSpacing(3)
        lbl = QtWidgets.QLabel(lbl_txt)
        lbl.setStyleSheet(_LABEL_SECTION)
        combo = QtWidgets.QComboBox()
        combo.setObjectName(attr)
        combo.setFixedHeight(32)
        combo.setStyleSheet(_SS_SELECT)
        combo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        combo.clear()
        for it in items:
            combo.addItem(it)
        setattr(ui, attr, combo)
        col.addWidget(lbl)
        col.addWidget(combo)
        date_row.addLayout(col)
    form_v.addLayout(date_row)
 
    ui.timeLabel = QtWidgets.QLabel("TIME OF TREATMENT")
    ui.timeLabel.setObjectName("timeLabel")
    ui.timeLabel.setStyleSheet(_LABEL_SECTION)
    form_v.addWidget(ui.timeLabel)

    for attr_h, attr_m, attr_ap, lbl_text in [
        ("hours",   "time",   "PM_or_AM",   "Start"),
        ("hours_2", "time_2", "PM_or_AM_2", "End"),
    ]:
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(5)
        tag = QtWidgets.QLabel(lbl_text)
        tag.setFixedWidth(36)
        tag.setStyleSheet(_LABEL_TIME)
        row.addWidget(tag)

        h_c = QtWidgets.QComboBox(); h_c.setObjectName(attr_h)
        h_c.setFixedHeight(32); h_c.setStyleSheet(_SS_SELECT)
        h_c.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        h_c.clear()
        for h in range(1, 13): h_c.addItem(f"{h:02d}")
        setattr(ui, attr_h, h_c); row.addWidget(h_c)

        sep = QtWidgets.QLabel(":")
        sep.setFixedWidth(8); sep.setAlignment(QtCore.Qt.AlignCenter)
        sep.setStyleSheet(
            f"color: {_MUTED}; font: 600 14pt 'Segoe UI'; background: transparent; border: none;")
        row.addWidget(sep)

        m_c = QtWidgets.QComboBox(); m_c.setObjectName(attr_m)
        m_c.setFixedHeight(32); m_c.setStyleSheet(_SS_SELECT)
        m_c.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        m_c.clear()
        for m in range(0, 60): m_c.addItem(f"{m:02d}")
        setattr(ui, attr_m, m_c); row.addWidget(m_c)

        ap_c = QtWidgets.QComboBox(); ap_c.setObjectName(attr_ap)
        ap_c.setFixedHeight(32); ap_c.setFixedWidth(62)
        ap_c.setStyleSheet(_SS_SELECT)
        ap_c.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        ap_c.addItems(["AM", "PM"])
        setattr(ui, attr_ap, ap_c); row.addWidget(ap_c)
        form_v.addLayout(row)

    
    chem_hdr = QtWidgets.QHBoxLayout()
    ui.chemLabel = QtWidgets.QLabel("CHEMICAL'S USED - TREATMENT")
    ui.chemLabel.setObjectName("chemLabel")
    ui.chemLabel.setStyleSheet(_LABEL_SECTION)
    chem_hdr.addWidget(ui.chemLabel); chem_hdr.addStretch()
    ui.ViewChem = QtWidgets.QPushButton("View all")
    ui.ViewChem.setObjectName("ViewChem")
    ui.ViewChem.setFixedHeight(24); ui.ViewChem.setStyleSheet(_SS_BTN_OUTLINE)
    ui.ViewChem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    chem_hdr.addWidget(ui.ViewChem)
    form_v.addLayout(chem_hdr)

    ui.chemicalUsed = QtWidgets.QTableWidget(5, 3)
    ui.chemicalUsed.setObjectName("chemicalUsed")
    ui.chemicalUsed.setMinimumHeight(168)
    ui.chemicalUsed.setStyleSheet(_SS_TABLE_MINI)
    ui.chemicalUsed.setAlternatingRowColors(True)
    ui.chemicalUsed.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    for r in range(5):
        ui.chemicalUsed.setVerticalHeaderItem(r, QtWidgets.QTableWidgetItem(str(r+1)))
    for c, t in enumerate(["Chemical/s used", "Quantity", "Remarks"]):
        ui.chemicalUsed.setHorizontalHeaderItem(c, QtWidgets.QTableWidgetItem(t))
    ui.chemicalUsed.horizontalHeader().setStretchLastSection(True)
    ui.chemicalUsed.horizontalHeader().setDefaultSectionSize(100)
    ui.chemicalUsed.verticalHeader().setDefaultSectionSize(32)
    form_v.addWidget(ui.chemicalUsed)

 
    act_hdr = QtWidgets.QHBoxLayout()
    ui.actualChemLabel = QtWidgets.QLabel("ACTUAL CHEMICAL ON HAND - TREATMENT")
    ui.actualChemLabel.setObjectName("actualChemLabel")
    ui.actualChemLabel.setStyleSheet(_LABEL_SECTION)
    act_hdr.addWidget(ui.actualChemLabel); act_hdr.addStretch()
    ui.ViewActChem = QtWidgets.QPushButton("View all")
    ui.ViewActChem.setObjectName("ViewActChem")
    ui.ViewActChem.setFixedHeight(24); ui.ViewActChem.setStyleSheet(_SS_BTN_OUTLINE)
    ui.ViewActChem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    act_hdr.addWidget(ui.ViewActChem)
    form_v.addLayout(act_hdr)

    ui.actualchemicalUsed = QtWidgets.QTableWidget(5, 3)
    ui.actualchemicalUsed.setObjectName("actualchemicalUsed")
    ui.actualchemicalUsed.setMinimumHeight(168)
    ui.actualchemicalUsed.setStyleSheet(_SS_TABLE_MINI)
    ui.actualchemicalUsed.setAlternatingRowColors(True)
    ui.actualchemicalUsed.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    for r in range(5):
        ui.actualchemicalUsed.setVerticalHeaderItem(r, QtWidgets.QTableWidgetItem(str(r+1)))
    for c, t in enumerate(["Actual chemical/s on hand", "Quantity", "Remarks"]):
        ui.actualchemicalUsed.setHorizontalHeaderItem(c, QtWidgets.QTableWidgetItem(t))
    ui.actualchemicalUsed.horizontalHeader().setStretchLastSection(True)
    ui.actualchemicalUsed.horizontalHeader().setDefaultSectionSize(100)
    ui.actualchemicalUsed.verticalHeader().setDefaultSectionSize(32)
    form_v.addWidget(ui.actualchemicalUsed)

    form_v.addSpacing(6)
    ui.confirmButton = QtWidgets.QPushButton("  Save record")
    ui.confirmButton.setObjectName("confirmButton")
    ui.confirmButton.setFixedHeight(38)
    ui.confirmButton.setStyleSheet(_SS_BTN_PRIMARY)
    ui.confirmButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    ci_px = QtGui.QPixmap(f"{image_path}/contentIcon.png")
    if not ci_px.isNull():
        ui.confirmButton.setIcon(QtGui.QIcon(ci_px))
        ui.confirmButton.setIconSize(QtCore.QSize(16, 16))
    form_v.addWidget(ui.confirmButton)
    form_v.addSpacing(12)

    form_scroll.setWidget(form_inner)
    cols.addWidget(form_scroll)

    ui.contentPanel = QtWidgets.QFrame()
    ui.contentPanel.setObjectName("contentPanel")
    ui.contentPanel.setStyleSheet(
        f"QFrame#contentPanel {{ background: {_BG}; border: none; }}")
    rp_v = QtWidgets.QVBoxLayout(ui.contentPanel)
    rp_v.setContentsMargins(14, 12, 14, 12)
    rp_v.setSpacing(10)

    rp_hdr = QtWidgets.QHBoxLayout()
    rp_title = QtWidgets.QLabel("Treatment records")
    rp_title.setStyleSheet(
        f"color: {_TEXT}; font: 600 12pt 'Segoe UI'; background: transparent; border: none;")
    rp_hdr.addWidget(rp_title); rp_hdr.addStretch()
    rp_v.addLayout(rp_hdr)

    table_frame = QtWidgets.QFrame()
    table_frame.setStyleSheet(
        f"QFrame {{ background: {_SURFACE}; border: 1px solid {_BORDER}; border-radius: 10px; }}")
    tf_v = QtWidgets.QVBoxLayout(table_frame)
    tf_v.setContentsMargins(0, 0, 0, 0)

    ui.tableListahan = QtWidgets.QTableWidget()
    ui.tableListahan.setObjectName("tableListahan")
    ui.tableListahan.setStyleSheet(_SS_TABLE_MAIN)
    ui.tableListahan.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    ui.tableListahan.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
    ui.tableListahan.setAlternatingRowColors(True)
    ui.tableListahan.setShowGrid(True)
    ui.tableListahan.setWordWrap(True)
    ui.tableListahan.setColumnCount(8)
    ui.tableListahan.setRowCount(1)
    ui.tableListahan.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem("1"))

    for col, (txt, w) in enumerate([
        ("Admin user", 350), ("Date of treatment", 350),
        ("Name of client", 350), ("Time of treatment", 350),
        ("Chemicals used", 350), ("Actual chemicals", 350),
        ("Remarks", 350), ("Edit", 100),
    ]):
        item = QtWidgets.QTableWidgetItem(txt)
        item.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Medium))
        ui.tableListahan.setHorizontalHeaderItem(col, item)
        ui.tableListahan.setColumnWidth(col, w)

    ui.tableListahan.horizontalHeader().setStretchLastSection(True)
    ui.tableListahan.horizontalHeader().setMinimumSectionSize(60)
    ui.tableListahan.verticalHeader().setDefaultSectionSize(48)
    tf_v.addWidget(ui.tableListahan)
    rp_v.addWidget(table_frame)

    cols.addWidget(ui.contentPanel, 1)
    page_v.addLayout(cols, 1)
    return page


# ─────────────────────────────────────────────────────────────────────────────
#  Main UI class
# ─────────────────────────────────────────────────────────────────────────────
class Ui_Dashboard(object):

    def setupUi(self, Dashboard):
        QtWidgets.QApplication.instance().setStyleSheet("""
           QToolTip {
                background-color: #2D6A4F;
                color: #ffffff;
                border: 1px solid #74C69D;
                border-radius: 5px;
                padding: 4px 8px;
                font: 10pt 'Segoe UI';
            }
        """)
        Dashboard.setObjectName("Dashboard")
        Dashboard.resize(1400, 900)
        Dashboard.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        Dashboard.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        Dashboard.setStyleSheet(f"QMainWindow {{ background: {_BG}; }}")

        cw = QtWidgets.QWidget(Dashboard)
        cw.setObjectName("centralwidget")
        cw.setStyleSheet(f"background: {_BG};")
        Dashboard.setCentralWidget(cw)

        root = QtWidgets.QVBoxLayout(cw)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── TITLE BAR ─────────────────────────────────────────────────────────
        self.titleBar = QtWidgets.QFrame()
        self.titleBar.setObjectName("titleBar")
        self.titleBar.setFixedHeight(56)
        self.titleBar.setStyleSheet(f"QFrame#titleBar {{ background: {_HEADER_BG}; }}")

        tb_h = QtWidgets.QHBoxLayout(self.titleBar)
        tb_h.setContentsMargins(0, 0, 0, 0)
        tb_h.setSpacing(0)

        # Hamburger toggle button (left edge of title bar)
        self._toggleBtn = QtWidgets.QPushButton("☰")
        self._toggleBtn.setFixedSize(52, 56)
        self._toggleBtn.setStyleSheet(_SS_TOGGLE_BTN + """
            QToolTip {
                background-color: #2D6A4F;
                color: #ffffff;
                border: 1px solid #74C69D;
                border-radius: 5px;
                padding: 4px 8px;
                font: 10pt 'Segoe UI';
            }
        """)
 
        self._toggleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._toggleBtn.setToolTip("Toggle sidebar")
        tb_h.addWidget(self._toggleBtn)

        tb_h.addSpacing(8)

        # Logo
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label")
        self.label.setFixedSize(60, 60)
        self.label.setStyleSheet("background: transparent; border: none;")
        logo_px = QtGui.QPixmap(f"{image_path}/Logo.png")
        if not logo_px.isNull():
            self.label.setPixmap(
                logo_px.scaled(48, 48, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.label.setScaledContents(True)
        else:
            self.label.setStyleSheet(f"background: {_G200}; border-radius: 6px; border: none;")
        tb_h.addWidget(self.label)
        tb_h.addSpacing(12)

        name_v = QtWidgets.QVBoxLayout()
        name_v.setSpacing(1)
        name_v.setContentsMargins(0, 0, 0, 0)
        self.appTitle_2 = QtWidgets.QLabel("RAIONN")
        self.appTitle_2.setObjectName("appTitle_2")
        self.appTitle_2.setStyleSheet(
            "color: #ffffff; font: 700 13pt 'Georgia'; "
            "background: transparent; letter-spacing: 2px;")
        name_v.addWidget(self.appTitle_2)
        sub = QtWidgets.QLabel("Pest Management System")
        sub.setStyleSheet(
            "color: rgba(198,246,213,0.50); font: 7pt 'Segoe UI'; "
            "background: transparent; letter-spacing: 0.5px;")
        name_v.addWidget(sub)
        tb_h.addLayout(name_v)
        tb_h.addStretch()

        self.windowControls = WindowControls()
        self.windowControls.setFixedSize(138, 56)
        self.windowControls.minimizeBtn.setFixedSize(46, 56)
        self.windowControls.maximizeBtn.setFixedSize(46, 56)
        self.windowControls.closeBtn.setFixedSize(46, 56)
        tb_h.addWidget(self.windowControls)
        root.addWidget(self.titleBar)

        # ── BODY ──────────────────────────────────────────────────────────────
        body_h = QtWidgets.QHBoxLayout()
        body_h.setContentsMargins(0, 0, 0, 0)
        body_h.setSpacing(0)

        # ── SIDEBAR (collapsible) ─────────────────────────────────────────────
        self.sidebar = CollapsibleSidebar()
        sb_v = QtWidgets.QVBoxLayout(self.sidebar)
        sb_v.setContentsMargins(0, 0, 0, 0)
        sb_v.setSpacing(0)

        nav_wrap = QtWidgets.QWidget()
        nav_wrap.setStyleSheet("background: transparent; border: none;")
        nav_v = QtWidgets.QVBoxLayout(nav_wrap)
        nav_v.setContentsMargins(0, 0, 0, 0)
        nav_v.setSpacing(2)

        # Section labels — stored so we can hide them when collapsed
        self._sec_modules  = _nav_section_lbl("REPORT TYPE")
        self._sec_storage  = _nav_section_lbl("TAB BINS")
        nav_v.addWidget(self._sec_modules)

        self.inspection      = _nav_btn("Inspection", f"{image_path}/Inspection.png")
        self.treatment       = _nav_btn("Treatment",  f"{image_path}/Treatment.png")
        nav_v.addWidget(self.inspection)
        nav_v.addWidget(self.treatment)

        nav_v.addWidget(self._sec_storage)
        self.actionPDF_STORAGE_3 = _nav_btn("Documents",   f"{image_path}/PDF.png")
        self.recycle_bin         = _nav_btn("Recycle Bin", f"{image_path}/Recycle Bin.png")
        nav_v.addWidget(self.actionPDF_STORAGE_3)
        nav_v.addWidget(self.recycle_bin)
        nav_v.addStretch()
        sb_v.addWidget(nav_wrap, 1)

        # Footer
        sb_footer = QtWidgets.QWidget()
        sb_footer.setStyleSheet(
            "background: transparent; border-top: 1px solid rgba(255,255,255,0.06);")
        sb_foot_v = QtWidgets.QVBoxLayout(sb_footer)
        sb_foot_v.setContentsMargins(8, 8, 8, 12)
        self.logout = QtWidgets.QPushButton("   Log out")
        self.logout.setObjectName("logout")
        self.logout.setFixedHeight(38)
        self.logout.setStyleSheet(_SS_LOGOUT_BTN)
        self.logout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        lgt_px = QtGui.QPixmap(f"{image_path}/Logout.png")
        if not lgt_px.isNull():
            self.logout.setIcon(QtGui.QIcon(lgt_px))
            self.logout.setIconSize(QtCore.QSize(16, 16))
        sb_foot_v.addWidget(self.logout)
        sb_v.addWidget(sb_footer)
        body_h.addWidget(self.sidebar)

        # ── NAV BUTTON GROUP — exactly one active at a time ───────────────────
        # All page-nav buttons (NOT logout — that's an action, not a page)
        self._nav_btns = [
            self.inspection,
            self.treatment,
            self.actionPDF_STORAGE_3,
            self.recycle_bin,
        ]
        self._active_nav = None   # track currently-active button

        def _activate(btn):
            """Mark btn as active, clear all others."""
            if self._active_nav is btn:
                return
            if self._active_nav is not None:
                self._active_nav.setStyleSheet(_SS_NAV_IDLE)
            self._active_nav = btn
            btn.setStyleSheet(_SS_NAV_ACTIVE)

        # Wire each nav button
        self.treatment.clicked.connect(lambda: _activate(self.treatment))
        self.inspection.clicked.connect(lambda: _activate(self.inspection))
        self.actionPDF_STORAGE_3.clicked.connect(
            lambda: _activate(self.actionPDF_STORAGE_3))
        self.recycle_bin.clicked.connect(lambda: _activate(self.recycle_bin))
        
        

        # Default active: Treatment
        _activate(self.treatment)

        # ── Content area ──────────────────────────────────────────────────────
        self.tabTreatment = _build_treatment_page(self)
        body_h.addWidget(self.tabTreatment, 1)
        root.addLayout(body_h, 1)

        # Wire toggle button
        self._toggleBtn.clicked.connect(self._toggle_sidebar)

        # Legacy stubs
        self.line   = QtWidgets.QFrame(cw); self.line.hide()
        self.line_8 = QtWidgets.QFrame(cw); self.line_8.hide()
        self.actionTREATMENT    = QtWidgets.QAction(Dashboard)
        self.actionINSPECTION   = QtWidgets.QAction(Dashboard)
        self.actionRECYCLE_BIN  = QtWidgets.QAction(Dashboard)
        self.actionPDF_STORAGE  = QtWidgets.QAction(Dashboard)
        self.actionLOGOUT       = QtWidgets.QAction(Dashboard)
        self.actionTREATMENT_2  = QtWidgets.QAction(Dashboard)
        self.actionINSPECTION_2 = QtWidgets.QAction(Dashboard)
        self.PDF_storage        = QtWidgets.QAction(Dashboard)
        self.label_12           = QtWidgets.QLabel(cw); self.label_12.hide()
        self.DocumentIcon       = QtWidgets.QLabel(cw); self.DocumentIcon.hide()
        self.trashIcon          = QtWidgets.QLabel(cw); self.trashIcon.hide()
        self.label_11           = QtWidgets.QLabel(cw); self.label_11.hide()
        self.HeaderTreatment    = QtWidgets.QLabel(cw); self.HeaderTreatment.hide()

        self.retranslateUi(Dashboard)
        QtCore.QMetaObject.connectSlotsByName(Dashboard)

    # ── Sidebar toggle ────────────────────────────────────────────────────────
    def _toggle_sidebar(self):
        self.sidebar.toggle()
        expanding = self.sidebar.is_expanded
        # Show/hide text labels on buttons after animation
        delay = 210 if expanding else 0
        QtCore.QTimer.singleShot(delay, lambda: self._update_sidebar_text(expanding))

    def _update_sidebar_text(self, show: bool):
        """Show or hide text labels and section headers in the sidebar."""
        for btn in self._nav_btns:
            label = btn.property("label") or ""
            btn.setText(f"   {label}" if show else "")
        self.logout.setText("   Log out" if show else "")
        self._sec_modules.setVisible(show)
        self._sec_storage.setVisible(show)

    # ── Draggable title bar ───────────────────────────────────────────────────
    def _install_drag(self, Dashboard):
        self._drag_pos = None

        def _press(e):
            if e.button() == QtCore.Qt.LeftButton:
                self._drag_pos = e.globalPos() - Dashboard.frameGeometry().topLeft()

        def _move(e):
            if e.buttons() == QtCore.Qt.LeftButton and self._drag_pos is not None:
                Dashboard.move(e.globalPos() - self._drag_pos)

        def _release(e):
            self._drag_pos = None

        self.titleBar.mousePressEvent   = _press
        self.titleBar.mouseMoveEvent    = _move
        self.titleBar.mouseReleaseEvent = _release

        self.windowControls.closeClicked.connect(Dashboard.close)
        self.windowControls.minimizeClicked.connect(Dashboard.showMinimized)
        self.windowControls.maximizeClicked.connect(
            lambda: Dashboard.showNormal()
            if Dashboard.isMaximized() else Dashboard.showMaximized())

    def retranslateUi(self, Dashboard):
        _t = QtCore.QCoreApplication.translate
        Dashboard.setWindowTitle(_t("Dashboard", "Raionn — Admin"))
        self.appTitle_2.setText(_t("Dashboard", "RAIONN"))
        self.HeaderTreatment.setText(_t("Dashboard", "New treatment entry"))
        self.nameLabel.setText(_t("Dashboard", "CLIENT - TREATMENT"))
        self.nameofClientinput.setPlaceholderText(_t("Dashboard", "e.g. Eorico"))
        self.dateLabel.setText(_t("Dashboard", "DATE OF TREATMENT"))
        self.timeLabel.setText(_t("Dashboard", "TIME OF TREATMENT"))
        self.chemLabel.setText(_t("Dashboard", "CHEMICAL'S USED - TREATMENT"))
        self.actualChemLabel.setText(_t("Dashboard", "ACTUAL CHEMICAL ON HAND - TREATMENT"))
        self.confirmButton.setText(_t("Dashboard", "  Save record"))
        self.searchDate.setPlaceholderText(_t("Dashboard", "Search client or date…"))
        self.confirmButton_2.setText(_t("Dashboard", "  Convert to PDF"))
        self.confirmButton_3.setText(_t("Dashboard", "  Trash"))
        self.ViewChem.setText(_t("Dashboard", "View all"))
        self.ViewActChem.setText(_t("Dashboard", "View all"))
        self.logout.setText(_t("Dashboard", "   Log out"))

        for col, txt in enumerate([
            "Admin user", "Date of treatment", "Name of client",
            "Time of treatment", "Chemicals used", "Actual chemicals",
            "Remarks", "Edit"
        ]):
            item = self.tableListahan.horizontalHeaderItem(col)
            if item:
                item.setText(_t("Dashboard", txt))

        self.actionTREATMENT.setText(_t("Dashboard", "TREATMENT"))
        self.actionINSPECTION.setText(_t("Dashboard", "INSPECTION"))
        self.actionRECYCLE_BIN.setText(_t("Dashboard", "RECYCLE BIN"))
        self.actionPDF_STORAGE.setText(_t("Dashboard", "DOCUMENT STORAGE"))
        self.actionLOGOUT.setText(_t("Dashboard", "LOGOUT"))
        self.actionTREATMENT_2.setText(_t("Dashboard", "TREATMENT"))
        self.actionINSPECTION_2.setText(_t("Dashboard", "INSPECTION"))
        self.PDF_storage.setText(_t("Dashboard", "DOCUMENT STORAGE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = QtWidgets.QMainWindow()
    ui  = Ui_Dashboard()
    ui.setupUi(win)
    ui._install_drag(win)
    win.showMaximized()
    sys.exit(app.exec_())