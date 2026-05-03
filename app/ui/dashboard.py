
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

base_dir   = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")


# ══════════════════════════════════════════════════════════════════════════════
#  Shared style constants
# ══════════════════════════════════════════════════════════════════════════════
_CLR_BG          = "#F0FAF4"
_CLR_PANEL_LEFT  = "#EAF7EE"
_CLR_PANEL_RIGHT = "#FFFFFF"
_CLR_PRIMARY     = "#2D6A4F"
_CLR_PRIMARY_DK  = "#1B4332"
_CLR_PRIMARY_XDK = "#081C15"
_CLR_ACCENT      = "#C6F6D5"
_CLR_TEXT        = "#1B4332"
_CLR_SUBTEXT     = "#6B8F78"
_CLR_BORDER      = "#D4E6DA"

_COMBO_SS = """
QComboBox {
    background-color: #FFFFFF;
    border: 1.5px solid #C6F6D5;
    border-bottom-color: #2D6A4F;
    border-right-color: #2D6A4F;
    border-radius: 7px;
    padding: 5px 10px;
    color: #1B4332;
    font: 10pt 'Segoe UI';
    min-height: 28px;
}
QComboBox:hover {
    background-color: #F0FAF4;
    border-bottom-color: #1B4332;
    border-right-color: #1B4332;
}
QComboBox:focus {
    border: 1.5px solid #2D6A4F;
    background-color: #F8FDF9;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1.5px solid #C6F6D5;
    border-radius: 6px;
    selection-background-color: #2D6A4F;
    selection-color: #ffffff;
    font: 10pt 'Segoe UI';
    padding: 2px;
}
"""

_INPUT_SS = """
QLineEdit {
    background-color: #FFFFFF;
    border: 1.5px solid #C6F6D5;
    border-bottom-color: #2D6A4F;
    border-right-color: #2D6A4F;
    border-radius: 8px;
    padding: 8px 12px;
    font: 11pt 'Segoe UI';
    color: #1B4332;
    selection-background-color: #C6F6D5;
}
QLineEdit:hover {
    background-color: #F4FBF7;
    border-bottom-color: #1B4332;
    border-right-color: #1B4332;
}
QLineEdit:focus {
    border: 1.5px solid #2D6A4F;
    background-color: #FFFFFF;
}
"""

_TABLE_SS = """
QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #F4FBF7;
    gridline-color: #E0EEE7;
    border: none;
    border-radius: 10px;
    font: 10pt 'Segoe UI';
    color: #1B4332;
    selection-background-color: #C6F6D5;
    selection-color: #1B4332;
}
QTableWidget::item {
    padding: 6px 10px;
    border: none;
}
QTableWidget::item:hover   { background-color: #E8F5EE; }
QTableWidget::item:selected { background-color: #C6F6D5; color: #1B4332; }
QHeaderView::section {
    background-color: #2D6A4F;
    color: #ffffff;
    border: none;
    border-right: 1px solid #1B4332;
    padding: 8px 10px;
    font: bold 10pt 'Segoe UI';
}
QHeaderView::section:vertical {
    background-color: #F0F7F2;
    color: #2D6A4F;
    border-bottom: 1px solid #D4E6DA;
    font: 9pt 'Segoe UI';
}
QHeaderView { background-color: transparent; border: none; }
QTableCornerButton::section { background-color: #2D6A4F; border: none; }
QScrollBar:vertical {
    background: #EAF5EF; width: 10px; border-radius: 5px; margin: 2px;
}
QScrollBar::handle:vertical {
    background: #74C69D; border-radius: 5px; min-height: 24px;
}
QScrollBar::handle:vertical:hover   { background: #2D6A4F; }
QScrollBar::handle:vertical:pressed { background: #1B4332; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
QScrollBar:horizontal {
    background: #EAF5EF; height: 10px; border-radius: 5px; margin: 2px;
}
QScrollBar::handle:horizontal {
    background: #74C69D; border-radius: 5px; min-width: 24px;
}
QScrollBar::handle:horizontal:hover   { background: #2D6A4F; }
QScrollBar::handle:horizontal:pressed { background: #1B4332; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
"""

_BTN_PRIMARY_SS = """
QPushButton {
    background-color: #2D6A4F;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font: bold 10pt 'Segoe UI';
    letter-spacing: 1px;
}
QPushButton:hover   { background-color: #1B4332; }
QPushButton:pressed { background-color: #081C15; }
QPushButton:disabled { background-color: #A8D5BA; color: rgba(255,255,255,0.6); }
"""

_BTN_DANGER_SS = """
QPushButton {
    background-color: #B91C1C;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    font: bold 9pt 'Segoe UI';
    letter-spacing: 1px;
}
QPushButton:hover   { background-color: #991B1B; }
QPushButton:pressed { background-color: #7F1D1D; }
"""

_BTN_WARNING_SS = """
QPushButton {
    background-color: #DC2626;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    font: bold 9pt 'Segoe UI';
    letter-spacing: 1px;
}
QPushButton:hover   { background-color: #B91C1C; }
QPushButton:pressed { background-color: #991B1B; }
"""

_BTN_PDF_SS = """
QPushButton {
    background-color: #1D4ED8;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    font: bold 9pt 'Segoe UI';
    letter-spacing: 1px;
}
QPushButton:hover   { background-color: #1E40AF; }
QPushButton:pressed { background-color: #1E3A8A; }
"""

_BTN_VIEW_SS = """
QPushButton {
    background-color: transparent;
    color: #2D6A4F;
    border: 1.5px solid #2D6A4F;
    border-radius: 6px;
    padding: 5px 10px;
    font: bold 9pt 'Segoe UI';
}
QPushButton:hover {
    background-color: #2D6A4F;
    color: #ffffff;
}
QPushButton:pressed { background-color: #1B4332; color: #ffffff; }
"""

_TOOLBAR_SS = """
QToolBar {
    background-color: #1B4332;
    border: none;
    border-right: 1px solid #0D2B1F;
    padding: 12px 6px;
    spacing: 8px;
}
QToolButton {
    background-color: transparent;
    color: rgba(198, 246, 213, 0.70);
    border-radius: 10px;
    padding: 8px;
    margin: 2px 4px;
}
QToolButton:hover {
    background-color: rgba(255, 255, 255, 0.12);
    color: #C6F6D5;
}
QToolButton:pressed {
    background-color: rgba(255, 255, 255, 0.22);
}
QToolButton:checked {
    background-color: rgba(198, 246, 213, 0.18);
    color: #C6F6D5;
    border-left: 3px solid #74C69D;
}
"""

_HEADER_SS = """
QFrame#headerBar {
    background-color: #2D6A4F;
    border-radius: 0px;
}
"""

_SECTION_CARD_SS = """
QFrame {
    background-color: #FFFFFF;
    border: 1px solid #D4E6DA;
    border-radius: 10px;
}
"""

_SECTION_LABEL_SS = (
    "background: transparent; border: none; "
    "color: #2D6A4F; font: bold 8pt 'Segoe UI'; letter-spacing: 2px;"
)

_FIELD_HEADING_SS = (
    "background: transparent; border: none; "
    "color: #1B4332; font: bold 11pt 'Segoe UI';"
)


def _section_label(parent, text):
    lbl = QtWidgets.QLabel(text, parent)
    lbl.setStyleSheet(_SECTION_LABEL_SS)
    return lbl


def _field_label(parent, text):
    lbl = QtWidgets.QLabel(text, parent)
    lbl.setStyleSheet(
        "background: transparent; border: none; "
        "color: #6B8F78; font: bold 8pt 'Segoe UI'; letter-spacing: 1px;"
    )
    return lbl


# ══════════════════════════════════════════════════════════════════════════════
#  UI class
# ══════════════════════════════════════════════════════════════════════════════
class Ui_Dashboard(object):

    def setupUi(self, Dashboard):
        Dashboard.setObjectName("Dashboard")
        Dashboard.resize(1462, 982)
        Dashboard.setStyleSheet(f"QMainWindow {{ background-color: {_CLR_BG}; }}")

        # ── Central widget ────────────────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(Dashboard)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(f"background-color: {_CLR_BG};")

        main_v = QtWidgets.QVBoxLayout(self.centralwidget)
        main_v.setContentsMargins(0, 0, 0, 0)
        main_v.setSpacing(0)

        # ══════════════════════════════════════════════════════════════════════
        #  HEADER BAR
        # ══════════════════════════════════════════════════════════════════════
        self.headerBar = QtWidgets.QFrame()
        self.headerBar.setObjectName("headerBar")
        self.headerBar.setFixedHeight(68)
        self.headerBar.setStyleSheet(_HEADER_SS)

        hdr_h = QtWidgets.QHBoxLayout(self.headerBar)
        hdr_h.setContentsMargins(16, 0, 20, 0)
        hdr_h.setSpacing(12)

        # Logo — bumped from 48×48 → 54×54
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label")
        self.label.setFixedSize(54, 54)
        self.label.setStyleSheet("background: transparent;")
        self.label.setPixmap(
            QtGui.QPixmap(f"{image_path}/Logo.png").scaled(
                54, 54, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        hdr_h.addWidget(self.label)

        # Vertical rule
        vline = QtWidgets.QFrame()
        vline.setFrameShape(QtWidgets.QFrame.VLine)
        vline.setFixedHeight(32)
        vline.setStyleSheet("color: rgba(198,246,213,0.30);")
        hdr_h.addWidget(vline)

        # App title
        self.appTitle_2 = QtWidgets.QLabel("RAIONN")
        self.appTitle_2.setObjectName("appTitle_2")
        self.appTitle_2.setStyleSheet(
            "color: #FFFFFF; font: bold 17pt 'Georgia'; "
            "background: transparent; letter-spacing: 3px;")
        hdr_h.addWidget(self.appTitle_2)

        # Sub-title
        sub = QtWidgets.QLabel("Admin System")
        sub.setStyleSheet(
            "color: rgba(198,246,213,0.55); font: 9pt 'Segoe UI'; "
            "background: transparent; letter-spacing: 1px;")
        hdr_h.addWidget(sub)

        hdr_h.addStretch()

        # Admin badge (right side)
        badge = QtWidgets.QWidget()
        badge.setStyleSheet("""
            QWidget {
                background-color: rgba(0,0,0,0.18);
                border-radius: 20px;
                border: 1px solid rgba(198,246,213,0.20);
            }
        """)
        badge_h = QtWidgets.QHBoxLayout(badge)
        badge_h.setContentsMargins(10, 4, 14, 4)
        badge_h.setSpacing(8)

        # Admin icon — bumped from 32×32 → 40×40
        self.adminIcon = QtWidgets.QLabel()
        self.adminIcon.setObjectName("adminIcon")
        self.adminIcon.setFixedSize(40, 40)
        self.adminIcon.setStyleSheet("background: transparent; border: none;")
        self.adminIcon.setPixmap(
            QtGui.QPixmap(f"{image_path}/adminIcon.png").scaled(
                40, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.adminIcon.setScaledContents(True)
        badge_h.addWidget(self.adminIcon)

        admin_info = QtWidgets.QVBoxLayout()
        admin_info.setSpacing(0)

        self.AdminName = QtWidgets.QLabel("ADMIN")
        self.AdminName.setObjectName("AdminName")
        self.AdminName.setStyleSheet(
            "color: #FFFFFF; font: bold 10pt 'Segoe UI'; "
            "background: transparent; border: none;")
        admin_info.addWidget(self.AdminName)

        role_lbl = QtWidgets.QLabel("Administrator")
        role_lbl.setStyleSheet(
            "color: rgba(198,246,213,0.55); font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")
        admin_info.addWidget(role_lbl)
        badge_h.addLayout(admin_info)
        hdr_h.addWidget(badge)

        main_v.addWidget(self.headerBar)

        # ══════════════════════════════════════════════════════════════════════
        #  BODY — toolbar + split panels
        # ══════════════════════════════════════════════════════════════════════
        body_h = QtWidgets.QHBoxLayout()
        body_h.setContentsMargins(0, 0, 0, 0)
        body_h.setSpacing(0)

        # ── Left toolbar ──────────────────────────────────────────────────────
        self.toolBar_files = QtWidgets.QToolBar(Dashboard)
        self.toolBar_files.setObjectName("toolBar_files")
        self.toolBar_files.setMovable(False)
        self.toolBar_files.setFloatable(False)
        self.toolBar_files.setOrientation(QtCore.Qt.Vertical)
        self.toolBar_files.setIconSize(QtCore.QSize(40, 40))  # unchanged
        self.toolBar_files.setStyleSheet(_TOOLBAR_SS)
        self.toolBar_files.setFixedWidth(72)
        Dashboard.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar_files)

        # Toolbar actions
        self.inspection = QtWidgets.QAction(Dashboard)
        self.inspection.setObjectName("inspection")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(f"{image_path}/Inspection.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inspection.setIcon(icon4)

        self.treatment = QtWidgets.QAction(Dashboard)
        self.treatment.setObjectName("treatment")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(f"{image_path}/Treatment.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.treatment.setIcon(icon3)

        self.recycle_bin = QtWidgets.QAction(Dashboard)
        self.recycle_bin.setObjectName("recycle_bin")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(f"{image_path}/Recycle Bin.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.recycle_bin.setIcon(icon1)

        self.actionPDF_STORAGE_3 = QtWidgets.QAction(Dashboard)
        self.actionPDF_STORAGE_3.setObjectName("actionPDF_STORAGE_3")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{image_path}/PDF.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPDF_STORAGE_3.setIcon(icon)

        self.logout = QtWidgets.QAction(Dashboard)
        self.logout.setObjectName("logout")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(f"{image_path}/Logout.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logout.setIcon(icon2)

        # Unused legacy actions (kept for backend compatibility)
        self.actionTREATMENT      = QtWidgets.QAction(Dashboard)
        self.actionTREATMENT.setObjectName("actionTREATMENT")
        self.actionINSPECTION     = QtWidgets.QAction(Dashboard)
        self.actionINSPECTION.setObjectName("actionINSPECTION")
        self.actionRECYCLE_BIN    = QtWidgets.QAction(Dashboard)
        self.actionRECYCLE_BIN.setObjectName("actionRECYCLE_BIN")
        self.actionPDF_STORAGE    = QtWidgets.QAction(Dashboard)
        self.actionPDF_STORAGE.setObjectName("actionPDF_STORAGE")
        self.actionLOGOUT         = QtWidgets.QAction(Dashboard)
        self.actionLOGOUT.setObjectName("actionLOGOUT")
        self.actionTREATMENT_2    = QtWidgets.QAction(Dashboard)
        self.actionTREATMENT_2.setObjectName("actionTREATMENT_2")
        self.actionINSPECTION_2   = QtWidgets.QAction(Dashboard)
        self.actionINSPECTION_2.setObjectName("actionINSPECTION_2")
        self.PDF_storage          = QtWidgets.QAction(Dashboard)
        self.PDF_storage.setObjectName("PDF_storage")
        self.PDF_storage.setIcon(icon)

        self.toolBar_files.addAction(self.inspection)
        self.toolBar_files.addAction(self.treatment)
        self.toolBar_files.addAction(self.recycle_bin)
        self.toolBar_files.addAction(self.actionPDF_STORAGE_3)

        # Spacer to push logout to bottom
        spacer_widget = QtWidgets.QWidget()
        spacer_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        spacer_widget.setStyleSheet("background: transparent;")
        self.toolBar_files.addWidget(spacer_widget)
        self.toolBar_files.addAction(self.logout)

        # ── Content area (scroll) ─────────────────────────────────────────────
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                background-color: #F0FAF4;
                border: none;
            }
            QScrollBar:vertical {
                background: #E0EEE7; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #74C69D; border-radius: 4px; min-height: 20px;
            }
            QScrollBar::handle:vertical:hover { background: #2D6A4F; }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height: 0; }
        """)

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setStyleSheet(
            f"background-color: {_CLR_BG};")

        scroll_h = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        scroll_h.setContentsMargins(12, 12, 12, 12)
        scroll_h.setSpacing(12)

        # ══════════════════════════════════════════════════════════════════════
        #  LEFT PANEL — Entry form
        # ══════════════════════════════════════════════════════════════════════
        left_panel = QtWidgets.QWidget()
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(420)
        left_panel.setStyleSheet("""
            QWidget#leftPanel {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #D4E6DA;
            }
        """)

        left_v = QtWidgets.QVBoxLayout(left_panel)
        left_v.setContentsMargins(18, 16, 18, 16)
        left_v.setSpacing(14)

        # ── Left panel header ─────────────────────────────────────────────────
        lhdr = QtWidgets.QWidget()
        lhdr.setStyleSheet("""
            QWidget {
                background-color: #F0FAF4;
                border-radius: 8px;
                border: 1px solid #C6F6D5;
            }
        """)
        lhdr_h = QtWidgets.QHBoxLayout(lhdr)
        lhdr_h.setContentsMargins(12, 10, 12, 10)
        lhdr_h.setSpacing(10)

        # Form icon — bumped from 28×28 → 34×34
        self.label_11 = QtWidgets.QLabel()
        self.label_11.setObjectName("label_11")
        self.label_11.setFixedSize(34, 34)
        self.label_11.setStyleSheet("background: transparent; border: none;")
        self.label_11.setPixmap(
            QtGui.QPixmap(f"{image_path}/filesIcon.png").scaled(
                34, 34, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label_11.setScaledContents(True)
        lhdr_h.addWidget(self.label_11)

        self.HeaderTreatment = QtWidgets.QLabel("NEW TREATMENT ENTRY")
        self.HeaderTreatment.setObjectName("HeaderTreatment")
        self.HeaderTreatment.setStyleSheet(
            "color: #1B4332; font: bold 12pt 'Segoe UI'; "
            "background: transparent; border: none; letter-spacing: 1px;")
        lhdr_h.addWidget(self.HeaderTreatment)
        lhdr_h.addStretch()
        left_v.addWidget(lhdr)

        # ── Section: Client ───────────────────────────────────────────────────
        left_v.addWidget(self._section_divider("CLIENT INFORMATION"))

        self.nameLabel = QtWidgets.QLabel("NAME OF CLIENT — TREATMENT")
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setStyleSheet(_SECTION_LABEL_SS)
        left_v.addWidget(self.nameLabel)

        self.nameofClientinput = QtWidgets.QLineEdit()
        self.nameofClientinput.setObjectName("nameofClientinput")
        self.nameofClientinput.setFixedHeight(42)
        self.nameofClientinput.setPlaceholderText("Ex: Eorico")
        self.nameofClientinput.setStyleSheet(_INPUT_SS)
        left_v.addWidget(self.nameofClientinput)

        # ── Section: Date ─────────────────────────────────────────────────────
        left_v.addWidget(self._section_divider("DATE OF TREATMENT"))

        self.dateLabel = QtWidgets.QLabel("DATE OF TREATMENT")
        self.dateLabel.setObjectName("dateLabel")
        self.dateLabel.setStyleSheet(_SECTION_LABEL_SS)
        left_v.addWidget(self.dateLabel)

        date_row = QtWidgets.QHBoxLayout()
        date_row.setSpacing(8)

        m_col = QtWidgets.QVBoxLayout()
        self.monthLabel = QtWidgets.QLabel("MONTH")
        self.monthLabel.setObjectName("monthLabel")
        self.monthLabel.setStyleSheet(_SECTION_LABEL_SS)
        m_col.addWidget(self.monthLabel)
        self.month = QtWidgets.QComboBox()
        self.month.setObjectName("month")
        self.month.setFixedHeight(40)
        self.month.setStyleSheet(_COMBO_SS)
        self.month.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for i in range(1, 13):
            self.month.addItem(str(i))
        m_col.addWidget(self.month)
        date_row.addLayout(m_col)

        d_col = QtWidgets.QVBoxLayout()
        self.dateCalLabel = QtWidgets.QLabel("DATE")
        self.dateCalLabel.setObjectName("dateCalLabel")
        self.dateCalLabel.setStyleSheet(_SECTION_LABEL_SS)
        d_col.addWidget(self.dateCalLabel)
        self.date = QtWidgets.QComboBox()
        self.date.setObjectName("date")
        self.date.setFixedHeight(40)
        self.date.setStyleSheet(_COMBO_SS)
        self.date.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for i in range(1, 32):
            self.date.addItem(str(i))
        d_col.addWidget(self.date)
        date_row.addLayout(d_col)

        y_col = QtWidgets.QVBoxLayout()
        self.yearLabel = QtWidgets.QLabel("YEAR")
        self.yearLabel.setObjectName("yearLabel")
        self.yearLabel.setStyleSheet(_SECTION_LABEL_SS)
        y_col.addWidget(self.yearLabel)
        self.year = QtWidgets.QComboBox()
        self.year.setObjectName("year")
        self.year.setFixedHeight(40)
        self.year.setStyleSheet(_COMBO_SS)
        self.year.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for yr in range(2015, 2031):
            self.year.addItem(str(yr))
        y_col.addWidget(self.year)
        date_row.addLayout(y_col)

        left_v.addLayout(date_row)

        # ── Section: Time ─────────────────────────────────────────────────────
        left_v.addWidget(self._section_divider("TIME OF TREATMENT"))

        self.timeLabel = QtWidgets.QLabel("TIME OF TREATMENT")
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setStyleSheet(_SECTION_LABEL_SS)
        left_v.addWidget(self.timeLabel)

        start_row = QtWidgets.QHBoxLayout()
        start_row.setSpacing(6)

        self.startTimeLabel = QtWidgets.QLabel("START")
        self.startTimeLabel.setObjectName("startTimeLabel")
        self.startTimeLabel.setFixedWidth(42)
        self.startTimeLabel.setStyleSheet(
            "color: #2D6A4F; font: bold 9pt 'Segoe UI'; "
            "background: transparent; border: none;")
        start_row.addWidget(self.startTimeLabel)

        self.hours = QtWidgets.QComboBox()
        self.hours.setObjectName("hours")
        self.hours.setFixedHeight(38)
        self.hours.setStyleSheet(_COMBO_SS)
        self.hours.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for h in range(1, 13):
            self.hours.addItem(f"{h:02d}")
        start_row.addWidget(self.hours)

        colon1 = QtWidgets.QLabel(":")
        colon1.setFixedWidth(10)
        colon1.setAlignment(QtCore.Qt.AlignCenter)
        colon1.setStyleSheet(
            "color: #2D6A4F; font: bold 14pt 'Segoe UI'; background: transparent; border: none;")
        start_row.addWidget(colon1)

        self.time = QtWidgets.QComboBox()
        self.time.setObjectName("time")
        self.time.setFixedHeight(38)
        self.time.setStyleSheet(_COMBO_SS)
        self.time.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for m in range(0, 60):
            self.time.addItem(f"{m:02d}")
        start_row.addWidget(self.time)

        self.PM_or_AM = QtWidgets.QComboBox()
        self.PM_or_AM.setObjectName("PM_or_AM")
        self.PM_or_AM.setFixedHeight(38)
        self.PM_or_AM.setStyleSheet(_COMBO_SS)
        self.PM_or_AM.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PM_or_AM.addItem("AM")
        self.PM_or_AM.addItem("PM")
        start_row.addWidget(self.PM_or_AM)
        left_v.addLayout(start_row)

        end_row = QtWidgets.QHBoxLayout()
        end_row.setSpacing(6)

        self.endTimeLabel = QtWidgets.QLabel("END")
        self.endTimeLabel.setObjectName("endTimeLabel")
        self.endTimeLabel.setFixedWidth(42)
        self.endTimeLabel.setStyleSheet(
            "color: #2D6A4F; font: bold 9pt 'Segoe UI'; "
            "background: transparent; border: none;")
        end_row.addWidget(self.endTimeLabel)

        self.hours_2 = QtWidgets.QComboBox()
        self.hours_2.setObjectName("hours_2")
        self.hours_2.setFixedHeight(38)
        self.hours_2.setStyleSheet(_COMBO_SS)
        self.hours_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for h in range(1, 13):
            self.hours_2.addItem(f"{h:02d}")
        end_row.addWidget(self.hours_2)

        colon2 = QtWidgets.QLabel(":")
        colon2.setFixedWidth(10)
        colon2.setAlignment(QtCore.Qt.AlignCenter)
        colon2.setStyleSheet(
            "color: #2D6A4F; font: bold 14pt 'Segoe UI'; background: transparent; border: none;")
        end_row.addWidget(colon2)

        self.time_2 = QtWidgets.QComboBox()
        self.time_2.setObjectName("time_2")
        self.time_2.setFixedHeight(38)
        self.time_2.setStyleSheet(_COMBO_SS)
        self.time_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for m in range(0, 61):
            self.time_2.addItem(f"{m:02d}")
        end_row.addWidget(self.time_2)

        self.PM_or_AM_2 = QtWidgets.QComboBox()
        self.PM_or_AM_2.setObjectName("PM_or_AM_2")
        self.PM_or_AM_2.setFixedHeight(38)
        self.PM_or_AM_2.setStyleSheet(_COMBO_SS)
        self.PM_or_AM_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PM_or_AM_2.addItem("AM")
        self.PM_or_AM_2.addItem("PM")
        end_row.addWidget(self.PM_or_AM_2)
        left_v.addLayout(end_row)

        # ── Section: Chemicals Used ───────────────────────────────────────────
        left_v.addWidget(self._section_divider("CHEMICALS USED"))

        chem_hdr = QtWidgets.QHBoxLayout()
        self.chemLabel = QtWidgets.QLabel("CHEMICALS USED — TREATMENT")
        self.chemLabel.setObjectName("chemLabel")
        self.chemLabel.setStyleSheet(_SECTION_LABEL_SS)
        chem_hdr.addWidget(self.chemLabel)
        chem_hdr.addStretch()
        self.ViewChem = QtWidgets.QPushButton("View All")
        self.ViewChem.setObjectName("ViewChem")
        self.ViewChem.setFixedHeight(28)
        self.ViewChem.setStyleSheet(_BTN_VIEW_SS)
        self.ViewChem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        chem_hdr.addWidget(self.ViewChem)
        left_v.addLayout(chem_hdr)

        self.chemicalUsed = QtWidgets.QTableWidget()
        self.chemicalUsed.setObjectName("chemicalUsed")
        self.chemicalUsed.setFixedHeight(200)
        self.chemicalUsed.setStyleSheet(_TABLE_SS)
        self.chemicalUsed.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.chemicalUsed.setAlternatingRowColors(True)
        self.chemicalUsed.setColumnCount(3)
        self.chemicalUsed.setRowCount(5)
        for r in range(5):
            self.chemicalUsed.setVerticalHeaderItem(r, QtWidgets.QTableWidgetItem(str(r + 1)))
        for c, txt in enumerate(["Chemical/s Used", "Quantity", "Remarks"]):
            item = QtWidgets.QTableWidgetItem(txt)
            self.chemicalUsed.setHorizontalHeaderItem(c, item)
        self.chemicalUsed.horizontalHeader().setStretchLastSection(True)
        self.chemicalUsed.horizontalHeader().setDefaultSectionSize(120)
        self.chemicalUsed.verticalHeader().setDefaultSectionSize(38)
        left_v.addWidget(self.chemicalUsed)

        # ── Section: Actual Chemicals ─────────────────────────────────────────
        act_hdr = QtWidgets.QHBoxLayout()
        self.actualChemLabel = QtWidgets.QLabel("ACTUAL CHEMICALS ON HAND — TREATMENT")
        self.actualChemLabel.setObjectName("actualChemLabel")
        self.actualChemLabel.setStyleSheet(_SECTION_LABEL_SS)
        act_hdr.addWidget(self.actualChemLabel)
        act_hdr.addStretch()
        self.ViewActChem = QtWidgets.QPushButton("View All")
        self.ViewActChem.setObjectName("ViewActChem")
        self.ViewActChem.setFixedHeight(28)
        self.ViewActChem.setStyleSheet(_BTN_VIEW_SS)
        self.ViewActChem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        act_hdr.addWidget(self.ViewActChem)
        left_v.addLayout(act_hdr)

        self.actualchemicalUsed = QtWidgets.QTableWidget()
        self.actualchemicalUsed.setObjectName("actualchemicalUsed")
        self.actualchemicalUsed.setFixedHeight(200)
        self.actualchemicalUsed.setStyleSheet(_TABLE_SS)
        self.actualchemicalUsed.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.actualchemicalUsed.setAlternatingRowColors(True)
        self.actualchemicalUsed.setColumnCount(3)
        self.actualchemicalUsed.setRowCount(5)
        for r in range(5):
            self.actualchemicalUsed.setVerticalHeaderItem(
                r, QtWidgets.QTableWidgetItem(str(r + 1)))
        for c, txt in enumerate(
                ["Actual Chemical/s on Hand", "Quantity", "Remarks"]):
            item = QtWidgets.QTableWidgetItem(txt)
            self.actualchemicalUsed.setHorizontalHeaderItem(c, item)
        self.actualchemicalUsed.horizontalHeader().setStretchLastSection(True)
        self.actualchemicalUsed.horizontalHeader().setDefaultSectionSize(120)
        self.actualchemicalUsed.verticalHeader().setDefaultSectionSize(38)
        left_v.addWidget(self.actualchemicalUsed)

        # ── Save button ───────────────────────────────────────────────────────
        save_row = QtWidgets.QHBoxLayout()
        save_row.setContentsMargins(0, 6, 0, 0)

        # Content icon — bumped from 28×28 → 34×34
        self.label_12 = QtWidgets.QLabel()
        self.label_12.setObjectName("label_12")
        self.label_12.setFixedSize(34, 34)
        self.label_12.setStyleSheet("background: transparent; border: none;")
        self.label_12.setPixmap(
            QtGui.QPixmap(f"{image_path}/contentIcon.png").scaled(
                34, 34, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label_12.setScaledContents(True)
        save_row.addWidget(self.label_12)

        self.confirmButton = QtWidgets.QPushButton("  SAVE RECORD")
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.setFixedHeight(44)
        self.confirmButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirmButton.setStyleSheet(_BTN_PRIMARY_SS)
        save_row.addWidget(self.confirmButton)
        left_v.addLayout(save_row)

        left_v.addStretch()
        scroll_h.addWidget(left_panel)

        # ══════════════════════════════════════════════════════════════════════
        #  RIGHT PANEL — Records table
        # ══════════════════════════════════════════════════════════════════════
        self.contentPanel = QtWidgets.QWidget()
        self.contentPanel.setObjectName("contentPanel")
        self.contentPanel.setStyleSheet("""
            QWidget#contentPanel {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #D4E6DA;
            }
        """)

        right_v = QtWidgets.QVBoxLayout(self.contentPanel)
        right_v.setContentsMargins(16, 14, 16, 14)
        right_v.setSpacing(12)

        # ── Toolbar row ───────────────────────────────────────────────────────
        toolbar_row = QtWidgets.QHBoxLayout()
        toolbar_row.setSpacing(10)

        search_wrap = QtWidgets.QWidget()
        search_wrap.setStyleSheet("""
            QWidget {
                background-color: #F4FBF7;
                border: 1.5px solid #D4E6DA;
                border-radius: 20px;
            }
        """)
        search_h = QtWidgets.QHBoxLayout(search_wrap)
        search_h.setContentsMargins(10, 0, 10, 0)
        search_h.setSpacing(6)

        # Search icon — bumped from 22×22 → 26×26
        self.searchIcon = QtWidgets.QLabel()
        self.searchIcon.setObjectName("searchIcon")
        self.searchIcon.setFixedSize(26, 26)
        self.searchIcon.setStyleSheet("background: transparent; border: none;")
        self.searchIcon.setPixmap(
            QtGui.QPixmap(f"{image_path}/searchIcon.png").scaled(
                26, 26, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.searchIcon.setScaledContents(True)
        search_h.addWidget(self.searchIcon)

        self.searchDate = QtWidgets.QLineEdit()
        self.searchDate.setObjectName("searchDate")
        self.searchDate.setFixedHeight(40)
        self.searchDate.setPlaceholderText("Search client or date...")
        self.searchDate.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                font: 10pt 'Segoe UI';
                color: #1B4332;
            }
        """)
        search_h.addWidget(self.searchDate)
        search_wrap.setFixedHeight(42)
        toolbar_row.addWidget(search_wrap, 1)

        toolbar_row.addStretch()

        # PDF icon — bumped from 24×24 → 30×30
        self.pdfIcon = QtWidgets.QLabel()
        self.pdfIcon.setObjectName("pdfIcon")
        self.pdfIcon.setFixedSize(60, 40)
        self.pdfIcon.setStyleSheet("background: transparent; border: none;")
        self.pdfIcon.setPixmap(
            QtGui.QPixmap(f"{image_path}/pdfIcon.png").scaled(
                60, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.pdfIcon.setScaledContents(True)

        self.confirmButton_2 = QtWidgets.QPushButton("CONVERT TO PDF")
        self.confirmButton_2.setObjectName("confirmButton_2")
        self.confirmButton_2.setFixedHeight(40)
        self.confirmButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirmButton_2.setStyleSheet(_BTN_PDF_SS)

        btn2_wrap = QtWidgets.QWidget()
        btn2_wrap.setStyleSheet("background: transparent; border: none;")
        btn2_h = QtWidgets.QHBoxLayout(btn2_wrap)
        btn2_h.setContentsMargins(0, 0, 0, 0)
        btn2_h.setSpacing(4)
        btn2_h.addWidget(self.pdfIcon)
        btn2_h.addWidget(self.confirmButton_2)
        toolbar_row.addWidget(btn2_wrap)

        # Trash icon — bumped from 24×24 → 30×30
        self.trashIcon = QtWidgets.QLabel()
        self.trashIcon.setObjectName("trashIcon")
        self.trashIcon.setFixedSize(60, 40)
        self.trashIcon.setStyleSheet("background: transparent; border: none;")
        self.trashIcon.setPixmap(
            QtGui.QPixmap(f"{image_path}/trashIcon.png").scaled(
                60, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.trashIcon.setScaledContents(True)

        self.confirmButton_3 = QtWidgets.QPushButton("TRASH")
        self.confirmButton_3.setObjectName("confirmButton_3")
        self.confirmButton_3.setFixedHeight(40)
        self.confirmButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirmButton_3.setStyleSheet(_BTN_DANGER_SS)

        btn3_wrap = QtWidgets.QWidget()
        btn3_wrap.setStyleSheet("background: transparent; border: none;")
        btn3_h = QtWidgets.QHBoxLayout(btn3_wrap)
        btn3_h.setContentsMargins(0, 0, 0, 0)
        btn3_h.setSpacing(4)
        btn3_h.addWidget(self.trashIcon)
        btn3_h.addWidget(self.confirmButton_3)
        toolbar_row.addWidget(btn3_wrap)

        right_v.addLayout(toolbar_row)

        # ── Thin divider ──────────────────────────────────────────────────────
        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.HLine)
        div.setStyleSheet("color: #E0EEE7; background-color: #E0EEE7; max-height: 1px; border: none;")
        right_v.addWidget(div)

        # ── Records table ─────────────────────────────────────────────────────
        self.tableListahan = QtWidgets.QTableWidget()
        self.tableListahan.setObjectName("tableListahan")
        self.tableListahan.setStyleSheet(_TABLE_SS)
        self.tableListahan.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableListahan.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.tableListahan.setAlternatingRowColors(True)
        self.tableListahan.setShowGrid(True)
        self.tableListahan.setWordWrap(True)

        self.tableListahan.setColumnCount(8)
        self.tableListahan.setRowCount(1)
        self.tableListahan.setVerticalHeaderItem(
            0, QtWidgets.QTableWidgetItem("1"))

        headers = [
            ("Admin User",                    110),
            ("Date of\nTreatment",            120),
            ("Name of Client\n(Treatment)",   160),
            ("Time of\nTreatment",            130),
            ("Chemical/s Used\n(Treatment)",  180),
            ("Actual Chemical/s\n(Treatment)",180),
            ("Remarks",                       150),
            ("Edit",                           80),
        ]
        for col, (txt, w) in enumerate(headers):
            item = QtWidgets.QTableWidgetItem(txt)
            item.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
            self.tableListahan.setHorizontalHeaderItem(col, item)
            self.tableListahan.setColumnWidth(col, w)

        self.tableListahan.horizontalHeader().setStretchLastSection(True)
        self.tableListahan.horizontalHeader().setMinimumSectionSize(60)
        self.tableListahan.verticalHeader().setDefaultSectionSize(56)

        right_v.addWidget(self.tableListahan)

        scroll_h.addWidget(self.contentPanel, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        body_h.addWidget(self.scrollArea)

        main_v.addLayout(body_h)
        Dashboard.setCentralWidget(self.centralwidget)

        # Unused geometry widgets kept as hidden stubs for backend compatibility
        self.line   = QtWidgets.QFrame(self.centralwidget)
        self.line.setObjectName("line")
        self.line.hide()
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setObjectName("line_8")
        self.line_8.hide()

        self.retranslateUi(Dashboard)
        QtCore.QMetaObject.connectSlotsByName(Dashboard)

    # ── Section divider helper ────────────────────────────────────────────────
    def _section_divider(self, label_text: str) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        w.setStyleSheet("background: transparent; border: none;")
        w.setFixedHeight(20)
        h = QtWidgets.QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)

        lbl = QtWidgets.QLabel(label_text)
        lbl.setStyleSheet(
            "color: #A0C4AE; font: bold 7pt 'Segoe UI'; "
            "letter-spacing: 2px; background: transparent; border: none;")
        h.addWidget(lbl)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setStyleSheet(
            "color: #D4E6DA; background-color: #D4E6DA; "
            "border: none; max-height: 1px;")
        h.addWidget(line)
        return w

    # ── retranslate ───────────────────────────────────────────────────────────
    def retranslateUi(self, Dashboard):
        _t = QtCore.QCoreApplication.translate
        Dashboard.setWindowTitle(_t("Dashboard", "Dashboard — Raionn Admin"))
        self.appTitle_2.setText(_t("Dashboard", "RAIONN"))
        self.AdminName.setText(_t("Dashboard", "ADMIN"))
        self.HeaderTreatment.setText(_t("Dashboard", "NEW TREATMENT ENTRY"))
        self.nameLabel.setText(_t("Dashboard", "NAME OF CLIENT — TREATMENT"))
        self.nameofClientinput.setPlaceholderText(_t("Dashboard", "Ex: Eorico"))
        self.dateLabel.setText(_t("Dashboard", "DATE OF TREATMENT"))
        self.monthLabel.setText(_t("Dashboard", "MONTH"))
        self.dateCalLabel.setText(_t("Dashboard", "DATE"))
        self.yearLabel.setText(_t("Dashboard", "YEAR"))
        self.timeLabel.setText(_t("Dashboard", "TIME OF TREATMENT"))
        self.startTimeLabel.setText(_t("Dashboard", "START"))
        self.endTimeLabel.setText(_t("Dashboard", "END"))
        self.chemLabel.setText(_t("Dashboard", "CHEMICALS USED — TREATMENT"))
        self.actualChemLabel.setText(_t("Dashboard", "ACTUAL CHEMICALS ON HAND — TREATMENT"))

        item = self.chemicalUsed.horizontalHeaderItem(0)
        item.setText(_t("Dashboard", "Chemical/s Used"))
        item = self.chemicalUsed.horizontalHeaderItem(1)
        item.setText(_t("Dashboard", "Quantity"))
        item = self.chemicalUsed.horizontalHeaderItem(2)
        item.setText(_t("Dashboard", "Remarks"))

        item = self.actualchemicalUsed.horizontalHeaderItem(0)
        item.setText(_t("Dashboard", "Actual Chemical/s on Hand"))
        item = self.actualchemicalUsed.horizontalHeaderItem(1)
        item.setText(_t("Dashboard", "Quantity"))
        item = self.actualchemicalUsed.horizontalHeaderItem(2)
        item.setText(_t("Dashboard", "Remarks"))

        self.confirmButton.setText(_t("Dashboard", "  SAVE RECORD"))
        self.searchDate.setPlaceholderText(_t("Dashboard", "Search client or date..."))
        self.confirmButton_2.setText(_t("Dashboard", "CONVERT TO PDF"))
        self.confirmButton_3.setText(_t("Dashboard", "TRASH"))
        self.ViewChem.setText(_t("Dashboard", "View All"))
        self.ViewActChem.setText(_t("Dashboard", "View All"))

        self.toolBar_files.setWindowTitle(_t("Dashboard", "Navigation"))
        self.inspection.setText(_t("Dashboard", "INSPECTION"))
        self.treatment.setText(_t("Dashboard", "TREATMENT"))
        self.recycle_bin.setText(_t("Dashboard", "RECYCLE BIN"))
        self.actionPDF_STORAGE_3.setText(_t("Dashboard", "PDF"))
        self.actionPDF_STORAGE_3.setShortcut(_t("Dashboard", "P"))
        self.logout.setText(_t("Dashboard", "LOGOUT"))

        self.actionTREATMENT.setText(_t("Dashboard", "TREATMENT"))
        self.actionINSPECTION.setText(_t("Dashboard", "INSPECTION"))
        self.actionRECYCLE_BIN.setText(_t("Dashboard", "RECYCLE BIN"))
        self.actionPDF_STORAGE.setText(_t("Dashboard", "PDF STORAGE"))
        self.actionLOGOUT.setText(_t("Dashboard", "LOGOUT"))
        self.actionTREATMENT_2.setText(_t("Dashboard", "TREATMENT"))
        self.actionINSPECTION_2.setText(_t("Dashboard", "INSPECTION"))
        self.PDF_storage.setText(_t("Dashboard", "PDF STORAGE"))

        item = self.tableListahan.verticalHeaderItem(0)
        item.setText(_t("Dashboard", "1"))
        headers_txt = [
            "Admin User", "Date of\nTreatment", "Name of Client\n(Treatment)",
            "Time of\nTreatment", "Chemical/s Used\n(Treatment)",
            "Actual Chemical/s\n(Treatment)", "Remarks", "Edit"
        ]
        for col, txt in enumerate(headers_txt):
            item = self.tableListahan.horizontalHeaderItem(col)
            if item:
                item.setText(_t("Dashboard", txt))


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Dashboard = QtWidgets.QMainWindow()
    ui = Ui_Dashboard()
    ui.setupUi(Dashboard)
    Dashboard.showMaximized()
    sys.exit(app.exec_())